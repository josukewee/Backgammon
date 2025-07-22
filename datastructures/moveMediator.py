from typing import Optional, Union
from datastructures.Bar import Bar
from datastructures.Board import Board
from datastructures.GameState import GameState
from datastructures.Home import Home
from datastructures.Stone import Stone


class MoveMediator:

    # validator for the moves, communicates with GameState(checkes turn conditions) and changes the Board datastructure
    def __init__(self, board: Board, game_state: GameState):
        self._board = board
        self._game_state = game_state

    def validate_move(self, from_stack: Union[int, Bar], to_stack: int) -> bool:
        # handles move conditions
        
        current_player = self._game_state.get_current_player
        current_dice = self._game_state.get_current_dice

        # are there stones on the bar that must be re-entered first? (Board)
        if self._board.get_bar_stones(current_player):
            if not isinstance(from_stack, Bar):
                return False
    
        distance = self._calculate_distance(from_stack, to_stack, current_player)

        # does the dice roll permit this move distance? 
        if distance not in current_dice:
            return False
        
        # handling right condition of bearing off
        if self.can_bear_off(current_player):
            if (current_player == "white" and to_stack == 25) or (current_player == "black" and to_stack == 0):
                # Allow overshoot if no stones are behind
                if self._no_stones_behind(from_stack, current_player):
                    max_die = max(current_dice)
                    if distance > max_die:
                        return True
                            
        # dest availability
        destination_stack = self._board.get_stack(to_stack)
        top_stones = destination_stack.get_stones

        if not top_stones:
            return True
        
        if len(top_stones) == 1:
            return True
        
        if top_stones[0].get_color == current_player:
            return True
        
        # all other conditions like distance is not rolled dice, there are stones behind when overshooting with bearing off
        return False

    def can_bear_off(self, color) -> bool:
        # all the stones are in the home(last 5 stacks)
        stacks = self._board.get_stacks

        home_range = range(0, 6) if color == "black" else range(19, 25)

        for i, stack in enumerate(stacks):
            # exclude home stacks
            if i in home_range:
                continue
            for stone in stack:
                if(stone.get_color == color):
                    return False
            return True

    def execute_move(self, from_stack: Union[int, Bar], to_stack: int) -> None:
        """Performs a legal move including hit, move, or bearing off."""
        current_player = self._game_state.get_current_player
        current_dice = self._game_state.get_current_dice

        # validate move
        if not self.validate_move(from_stack, to_stack):
            raise ValueError(f"Invalid move from stack index: {from_stack} to stack index: {to_stack} by {current_player}")
        
        distance = self._calculate_distance(from_stack, to_stack, current_player)
        stone = self._board.get_stack(from_stack).peek_stone()

        if distance in current_dice:
            current_dice.remove(distance)
        else:
            # overshoot since we know it's allowed due to validate_move
            max_die = max(current_dice)
            current_dice.remove(max_die)

        # bar move
        if isinstance(from_stack, Bar):
            self.proccess_bar(from_stack, to_stack)
            return

        # bearing off
        if self.can_bear_off(current_player):
            if (current_player == "white" and to_stack == 25) or (current_player == "black" and to_stack == 0):
                self._board.move_stone(stone, self._board.get_home[stone.color])
                return

        # hitting
        if self._is_hit(to_stack, current_player):
            self.hit_stone(to_stack)

        self._board.move_stone(stone, to_stack)


    def hit_stone(self, to_stack: int) -> Optional[Stone]:

        current_player = self._game_state.get_current_player()

        if self._is_hit(to_stack, current_player):
            stack = self._board.get_stack(to_stack)
            stone = stack.peek_stone()
            self._board.move_stone(stone, self._board.get_bar)

            return stone

        return None

    def proccess_bar(self, from_bar: Bar, to_stack: int) -> None:
        current_player = self._game_state.get_current_player()
        
        stone = from_bar.get_stones(current_player).pop()

        if self._is_hit(to_stack, current_player):
            stone = self._board.get_stack(to_stack).peek_stone()
            self._board.move_stone(stone, self._board.get_bar)
        
        self._board.get_stack(to_stack).add_stone(stone)
        self._board.update_stone_location(stone, self._board.get_stack(to_stack))

    def _no_stones_behind(self, from_stack: int, color: str) -> bool:
        #  handles overshoot when bearing off

        stacks = self._board.get_stacks()
        
        if color == "white":
            behind_range = range(from_stack + 1, 24)  # stacks higher than current
        else:
            behind_range = range(from_stack - 1, -1, -1)  # stacks lower than current

        for i in behind_range:
            for stone in stacks[i].get_stones():
                if stone.get_color() == color:
                    return False
        return True

    def _calculate_distance(self, from_stack: Union[int, Bar], to_stack: int, player_color: str) -> int:
        
        if isinstance(from_stack, int):

            if not (1 <= from_stack <= 24 and 1 <= to_stack <= 24):
                raise ValueError("Stack indexes must be in range 1 to 24")
            
            distance = to_stack - from_stack if player_color == "white" else from_stack - to_stack
        
        elif isinstance(from_stack, Bar):
            entry_point = 0 if player_color == "white" else 25
            distance = abs(to_stack - entry_point)

        else:
            raise TypeError("from_stack must be type of int or Bar")
        
        if distance <= 0:
                raise ValueError(f"Invalid move direction for {player_color}. Distance: {distance}")
        
        return distance

    def _is_hit(self, to_stack: int, player_color: str) -> bool:
        stack = self._board.get_stack(to_stack)
        top_stone = stack.peek_stone()

        if top_stone and len(stack.get_stones()) == 1:
            return top_stone.get_color() != player_color

        return False
    