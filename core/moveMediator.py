from typing import Optional, Union
from datastructures.Bar import Bar
from datastructures.Board import Board
from core.gameState import GameState
from datastructures.Home import Home
from datastructures.Stone import Stone


class MoveMediator:

    # validator for the moves, communicates with GameState(checkes turn conditions) and changes the Board datastructure
    def __init__(self, board: Board, game_state: GameState):
        self._board = board
        self._game_state = game_state

    def validate_move(self, from_stack: Union[int, Bar], to_stack: int) -> bool:

        current_player = self._game_state.get_current_player
        current_dice = self._game_state.get_current_dice

        # If bar has stones, must re-enter
        if self._board.get_bar_stones(current_player):
            if not isinstance(from_stack, Bar):
                return False

        # calculate distance
        try:
            distance = self._calculate_distance(from_stack, to_stack, current_player)
        except ValueError:
            print("failed here")
            return False 

        # check if dice allow this move (except overshoot for bear-off)
        if distance not in current_dice:
            # allow overshoot ONLY if bearing off and no stones behind
            if (self.can_bear_off(current_player) and
                    self._is_bear_off_move(from_stack, to_stack, distance, current_dice, current_player)):
                return True

        # validate destination
        # bearing off
        if self._is_bearing_off(to_stack, current_player):
            return self.can_bear_off(current_player)

        # normal move
        destination_stack = self._board.get_stack(to_stack)
        stones = destination_stack.get_stones

        # empty → allowed
        if not stones:
            return True

        # same color and < 5 stones → allowed
        if stones[0].get_color == current_player and len(stones) < 5:
            return True

        # hit one stone of opposite color
        if len(stones) == 1 and stones[0].get_color != current_player:
            return True

        # otherwise blocked
        return False

    def _is_bearing_off(self, to_stack: int, player_color: str) -> bool:
        return (player_color == "white" and to_stack == 0) or \
            (player_color == "black" and to_stack == 25)

    def _is_bear_off_move(self, from_stack: int, to_stack: int, distance: int, dice: list[int], player_color: str) -> bool:

        # check if it's going to the bear-off "stack"
        if player_color == "white" and to_stack != 25:
            return False
        if player_color == "black" and to_stack != 0:
            return False

        # check no stones behind
        if not self._no_stones_behind(from_stack, player_color):
            return False

        # overshoot only if distance is greater than all dice values
        return any(d >= distance for d in dice)

    def can_bear_off(self, color: str) -> bool:
        # quick bar check
        if self._board.get_bar_stones(color):
            return False

        # home quadrants in point numbers (1..24)
        home_points = set(range(1, 7)) if color == "black" else set(range(19, 25))

        stacks = list(self._board.get_stacks)
        for pt in range(1, 25):
            if pt in home_points:
                continue
            stones = stacks[pt - 1].get_stones
            for s in stones:
                # print(f"{s.get_color} sotne color, player color: {color}")
                if s.get_color != color:
                    # print("failed here")
                    return False
        return True

    def execute_move(self, from_stack: Union[int, Bar], to_stack: int) -> tuple[Stone, Optional[Stone]]:
        """Performs a legal move including hit, move, or bearing off."""
        current_player = self._game_state.get_current_player
        hit_stone = None

        # validate move
        if not self.validate_move(from_stack, to_stack):
            raise ValueError(f"Invalid move from stack index: {from_stack} to stack index: {to_stack} by {current_player}")
        
        distance = self._calculate_distance(from_stack, to_stack, current_player)

        # bar move
        if isinstance(from_stack, Bar):
            moved_stone, hit_stone = self._process_bar_move(from_stack, to_stack)
            return moved_stone, hit_stone

        stone = self._board.get_stack(from_stack).peek_stone()

        # bearing off home is incexed 0 for black and 25 for white
        if self.can_bear_off(current_player):
            if (current_player == "white" and to_stack == 25) or (current_player == "black" and to_stack == 0):
                self._board.move_stone(stone, self._board.get_home[stone.color])
                return stone, None

        # hitting
        if self._is_hit(to_stack, current_player):
            hit_stone = self.hit_stone(to_stack)

        # print(f"DEBUG: About to move stone from stack {from_stack} to {to_stack}")
        # print(f"DEBUG: stone ref: {stone}, color: {stone.get_color}")
        print(f"DEBUG: board location of stone: {self._board._stone_location.get(stone)}")

        # Basic condition
        self._board.move_stone(stone, to_stack)

        print("DEBUG BOARD STATE:")
        for i in range(1, 25):
            stones = [s.get_color for s in self._board.get_stack(i).get_stones]
            if stones:
                print(f"Stack {i}: {stones}")
            print(self._board._bar)
        return stone, hit_stone 

    def move_stone(self, stone: Stone, from_stack: Union[int, Bar, Home], to_stack: Union[int, Bar, Home]):
        """Bypasses full validation logic. Used for undo operations."""

       
        if isinstance(from_stack, Home):
            from_stack.force_remove_stone(stone)
        else:
            from_stack.remove_stone(stone)

        if isinstance(to_stack, int):
            target_stack = self._board.get_stack(to_stack)
            target_stack.add_stone(stone)
            self._board.update_stone_location(stone, target_stack)
        else:
            to_stack.add_stone(stone)
            self._board.update_stone_location(stone, to_stack)

    def hit_stone(self, to_stack: int) -> Optional[Stone]:

        current_player = self._game_state.get_current_player

        if self._is_hit(to_stack, current_player):
            stack = self._board.get_stack(to_stack)
            stone = stack.peek_stone()
            self._board.move_stone(stone, self._board.get_bar)

            return stone

        return None

    def _process_bar_move(self, from_bar: Bar, to_stack: int) -> tuple[Stone, Optional[Stone]]:
        current_player = self._game_state.get_current_player
        hit_stone = None

        # take last stone of current player from bar
        stone = from_bar.get_stones(current_player)[-1]

        # hitting
        if self._is_hit(to_stack, current_player):
            hit_stone = self._board.get_stack(to_stack).peek_stone()
            self._board.move_stone(hit_stone, self._board.get_bar)

        self._board.move_stone(stone, to_stack)

        return stone, hit_stone

    def _no_stones_behind(self, from_stack: int, color: str) -> bool:
        #  handles overshoot when bearing off

        stacks = self._board.get_stacks
        
        if color == "white":
            behind_range = range(from_stack + 1, 24)  # stacks higher than current
        else:
            behind_range = range(from_stack - 1, -1, -1)  # stacks lower than current

        for i in behind_range:
            for stone in stacks[i].get_stones:
                if stone.get_color == color:
                    return False
        return True

    def _calculate_distance(self, from_stack: Union[int, Bar], to_stack: int, player_color: str) -> int:

        # special case: bearing off
        if to_stack == 25 and player_color == "white":
            return from_stack  
        if to_stack == 0 and player_color == "black":
            return 25 - from_stack 

        # bar move
        if isinstance(from_stack, Bar):

            if player_color == "white":
                return 25 - to_stack
            else:
                return to_stack
            
        # normal move
        if player_color == "white":
            distance = from_stack - to_stack
        else:
            distance = to_stack - from_stack

        if distance <= 0:
            return -1  
        return distance


    def _is_hit(self, to_stack: int, player_color: str) -> bool:
        stack = self._board.get_stack(to_stack)

        if stack.is_empty():
            return False

        top_stone = stack.peek_stone()

        if top_stone and len(stack.get_stones) == 1:
            return top_stone.get_color != player_color

        return False
    