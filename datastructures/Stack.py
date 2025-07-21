from datastructures.Stone import Stone
from collections import deque

class Stack:
    # stack is purely the datastructure that knows no gamelogic

    def __init__(self, index, *stones: Stone):
        self.index = index
        self._elements = deque(stones, maxlen = 5)

    def add_stone(self, stone: Stone) -> bool:
        self._elements.append(stone)
            
    def remove_last_stone(self) -> Stone:
        return self._elements.pop()
        
    def remove_first_stone(self) -> bool:
        self._elements.popleft()

    def peek_stone(self) -> Stone:
        return self._elements[-1]
    
    @property
    def get_stones(self):
        return self._elements

    def __repr__(self):
        stones_list = [repr(stone) for stone in self._elements]
        return f"Stack {self.index}"