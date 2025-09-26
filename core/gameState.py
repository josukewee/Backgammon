from random import randint
from typing import Optional
from datastructures import Dice
from datastructures.Board import Board

class GameState:
    def __init__(self):
        self._current_player = "white"
        self._dice = (1, 1)
        # self._real_dice = Dice()
        self._has_rolled = False
        self._doubling_cube = 1
        self._winner = None

    def next_turn(self) -> None:
        """Swaps the current player and resets turn-specific state."""
        self._current_player = "black" if self._current_player == "white" else "white"
        self._has_rolled = False
        self._dice = (1, 1)  # Reset dice

    def roll_dice(self) -> tuple[int, int]:
        """Rolls two dice for the current player."""
        if self._has_rolled:
            raise ValueError("Already rolled this turn!")
        self._dice = (randint(1, 6), randint(1, 6))
        self._has_rolled = True
        return self._dice

    def is_double(self) -> bool:
        """Checks if the current roll is doubles (e.g., [4, 4])."""
        return self._dice[0] == self._dice[1]
    
    @property
    def get_current_player(self):
        return self._current_player
    
    @property
    def get_current_dice(self):
        return self._dice

    
    def check_winner(self, board: Board) -> Optional[str]:
        """Returns 'white', 'black', or None if no winner yet."""
        white_home = board.get_home["white"]
        black_home = board.get_home["black"]

        if len(white_home.get_stones) == 15:
            self._winner = "white"
        elif len(black_home.get_stones) == 15:
            self._winner = "black"
        else:
            self._winner = None

        return self._winner