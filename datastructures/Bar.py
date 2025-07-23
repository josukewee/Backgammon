from datastructures.Stone import Stone
from datastructures.interfaces import StoneContainer

class Bar(StoneContainer):
    def __init__(self):
        self._bars = {"white": [], "black": []}

    def must_reenter(self, color) -> bool:
        """Checkes if the bar of passed color has any stones in it"""
        return len(self._bars[color]) > 0

    def add_stone(self, stone: Stone) -> None:
        self._bars[stone.get_color].append(stone)

    def remove_stone(self, stone: Stone):
        self._bars[stone.get_color].remove(stone)

    def get_stones(self, color: str) -> Stone:
        return self._bars[color]

    def get_bar(self, color: str):
        self._bars[color]

    def __repr__(self):
        return f"White: {self._bars['white']}, black: {self._bars['black']}"
