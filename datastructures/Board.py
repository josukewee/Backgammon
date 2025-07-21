from itertools import count
from datastructures.Stack import Stack
from datastructures.Stone import Stone
from datastructures.Bar import Bar
from datastructures.Home import Home

from typing import Iterator, Union


class Board:
    # facade that carries all the predefined datastructers
    # orchastrates the behavior between stones, pieces, bar

    STACK_NUM = 24

    def __init__(self):
        self._stacks = []
        self._bar = Bar()
        self._stone_location: dict[Stone, Union[Stack, Bar, Home]] = {}
        # add home for both parties
        self._home = Home()

        self._init_structures()

    # probably will need to create an abstract factory if the rules and board is going to be custom, now is not required
    def _init_structures(self):
        self._stacks = [Stack(i) for i in range (1, 25)]

        self._place_stones()

    def _place_stones(self):
        uid_generator = count(start=1)
        initial_layout = [
            (1, 2, "black"), (6, 5, "white"), (8, 3, "white"),
            (12, 5, "black"), (13, 5, "white"), (17, 3, "black"),
            (19, 5, "black"), (24, 2, "white")
        ]
        # bar_stone_example = Stone(31, "white")
        # self.bar.add_stone(bar_stone_example)
        # self._stone_location[bar_stone_example] = self._bar

        

        for index, number_of_pieces, color in initial_layout:
            stack = self._stacks[index - 1] # stack itself stores the 0-index values

            for _ in range(number_of_pieces):
                stone = Stone(next(uid_generator), color)
                self._stone_location[stone] = stack
                stack.add_stone(stone)
    
    def move_stone(self, stone: Stone, target: int) -> None:
        # probably needs to update imput stone to stone_uid
        if not (1 <= target <= self.STACK_NUM):
            raise ValueError("Stack number should be within 1 and 24")

        # remove from current possition(stack, bar, Home)
        self._stone_location[stone].remove_last_stone()
        # current
        target_stack = self._stacks[target - 1]
        target_stack.add_stone(stone)
        # add to the new possiton
        self._stone_location[stone] = target_stack

    def move_to_bar(self, stone: Stone) -> None:
        origin = self._stone_location[stone]
        origin.remove_stone(stone)
        self._bar.add_stone(stone)
        self._stone_location[stone] = self._bar

    def move_to_home(self, stone: Stone) -> None:
        origin = self._stone_location[stone]
        origin.remove_stone(stone)
        self._home[stone.color].add_stone(stone)
        self._stone_location[stone] = self._home


    # GETTERS
    def get_stone_location(self, stone: Stone) -> Union[Stack, Bar, Home]:
        return self._stone_location.get(stone)
    
    def get_stack(self, index: int) -> Stack:
        if not (1 <= index <= self.NUM_POINTS):
            raise ValueError(f"Stack index {index} out of range")
        return self._stacks[index - 1]

    def get_bar_stones(self, color: str) -> list[Stone]:
        return self._bar[color]
    

def test():
    board = Board()
    # print(board._stone_location)
    # for stack in board.get_stacks:
    print(board._stone_location)
    some_stone = board._stacks[0].peek_piece()
    board.move_stone(some_stone, 3)
    print(board._stone_location)

test()