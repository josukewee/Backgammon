from datastructures.Stone import Stone
from datastructures.interfaces import StoneContainer

from collections import deque

class Stack(StoneContainer):
    # stack is purely the datastructure that knows no gamelogic

    def __init__(self, index, *stones: Stone):
        self.index = index
        self._elements = deque(maxlen = 5)

        for stone in stones:
            self.add_stone(stone)

    def add_stone(self, stone: Stone) -> bool:
        if not isinstance(stone, Stone):
            raise TypeError(f"Expected Stone, got {type(stone).__name__}")
        
        self._elements.append(stone)


    def remove_last_stone(self) -> Stone:
        return self._elements.pop()
          
    def remove_stone(self, stone: Stone) -> Stone:
        return self._elements.remove(stone)
      
    def peek_stone(self) -> Stone:
        return self._elements[-1]
    
    def is_empty(self) -> bool:
        return len(self._elements) == 0
    
    @property
    def get_stones(self):
        return self._elements

    def __repr__(self):
        stones_list = [repr(stone) for stone in self._elements]
        return f"Stack {self.index}"
    
    def __iter__(self):
        return iter(self._elements)