from typing import Literal
from abc import ABC, abstractmethod
from datastructures.Stone import Stone 

class StoneContainer(ABC):
    @abstractmethod
    def add_stone(self, stone: Stone) -> None:
        pass

    @abstractmethod
    def remove_stone(self, stone: Stone) -> None:
        pass

Color = Literal["white", "black"]


__all__ = ["Color"]