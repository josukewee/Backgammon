from datastructures.Stone import Stone

class Home:
    def __init__(self):
        self._pieces: dict[str, list[Stone]] = {"white": [], "black": []}  # Clean and explicit

    def add_piece(self, stone: Stone) -> None:
        """Adds a stone to the correct player's home."""
        self._pieces[stone.color].append(stone)

    def get_pieces(self, color: str) -> list[Stone]:
        """Returns all stones borne off by a player."""
        return self._pieces[color]

    def has_all_pieces(self, color: str, total_pieces: int = 15) -> bool:
        """Checks if a player has borne off all their pieces."""
        return len(self._pieces[color]) >= total_pieces