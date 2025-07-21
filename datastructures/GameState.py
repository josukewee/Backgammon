from random import randint
from typing import Optional
from datastructures.Board import Board

class GameState:
    def __init__(self):
        self._current_player = "white"  # or "black"
        self._dice = (1, 1)            # Current roll (default values)
        self._has_rolled = False       # Must roll before moving
        self._doubling_cube = 1        # Starts at 1x (no double)
        self._winner = None            # Track winner ("white", "black", or None)

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

    # --- Win Conditions ---
    def check_winner(self, board: Board) -> Optional[str]:
        """Returns "white", "black", or None if no winner yet."""
        if board.home.has_all_pieces("white"):
            self._winner = "white"
        elif board.home.has_all_pieces("black"):
            self._winner = "black"
        return self._winner