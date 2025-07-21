from typing import Union
from datastructures.Bar import Bar
from datastructures.Board import Board
from datastructures.GameState import GameState


class MoveMediator:

    # validator for the moves, communicates with GameState(checkes turn conditions) and changes the Board datastructure
    def __init__(self, board: Board, game_state: GameState):
        self._board = board
        self._game_state = game_state

    def validate_move(self, from_stack: Union[int, Bar], to_stack: int) -> bool:
        # handles move conditions
        current_player = self._game_state.get_current_player
        current_dice = self._game_state.get_current_dice

        # 1. Is it the player's turn? (GameState)
        if self._board.get_bar_stones(current_player):
            if not isinstance(from_stack, Bar):
                return False
    
        # 2. Are there stones on the bar that must be re-entered first? (Board)
        # 3. Does the dice roll permit this move distance? (GameState)
        distance = self._calculate_distance(from_stack, to_stack, current_player)

        if distance not in current_dice:
            return False
        # 4. Is the destination stack open or hittable? (Board)
        destination_stack = self._board.get_stack(to_stack)
        top_stones = destination_stack.get_stones

        if not top_stones:
            return True
        
        if len(top_stones) == 1:
            return True
        
        if top_stones[0].get_color == current_player:
            return True
        
        
        return False

    def can_bear_off(self, color) -> bool:
        # all the stones are in the home(last 5 stacks)
        ...

    def execute_move(self, from_stack: int, to_stack: int):
        ...

    def hit_stone(self, to_stack):
        # detects when the stone is hit and sending it to the bar
        ...

    def proccess_bar(self, from_bar, to_stack):
        #  handles getting off the bar and making it mandatory to have it empty
        ...

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
    