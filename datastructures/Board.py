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
        # since the bar implementaion requires stack 0 and 25 might change that in the future
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
    
    # probably needs to update imput stone to stone_uid
    def move_stone(self, stone: Stone, target: Union[int, Bar, Home]) -> None:
        origin = self._stone_location[stone]

        if isinstance(origin, Home):
            raise TypeError("Cannot move a stone from home")

        # remove stone from its origin (shared interface)
        origin.remove_stone(stone)

        # moving to another Stack
        if isinstance(target, int):
            if not (1 <= target <= self.STACK_NUM):
                raise ValueError("Target stack number must be between 1 and 24")
            target_stack = self._stacks[target - 1]
            target_stack.add_stone(stone)
            self._stone_location[stone] = target_stack

        # moving to Bar (usually on hit)
        elif isinstance(target, Bar):
            target.add_stone(stone)
            self._stone_location[stone] = target

        # bearing off to Home
        elif isinstance(target, Home):
            target.add_stone(stone)
            self._stone_location[stone] = target

        else:
            raise TypeError(f"Invalid target type: {type(target)}")
        
        

    def update_stone_location(self, stone: Stone, location: Union[Stack, Bar, Home]) -> None:
        self._stone_location[stone] = location


    # GETTERS
    def get_stone_location(self, stone: Stone) -> Union[Stack, Bar, Home]:
        return self._stone_location.get(stone)
    
    def get_stack(self, index: int) -> Stack:
        if not (0 <= index <= 25):
            raise ValueError(f"Stack index {index} out of range")
        return self._stacks[index - 1]

    def get_bar_stones(self, color: str) -> list[Stone]:
        return self._bar.get_stones(color)
    
    @property
    def get_stacks(self) -> list[Stack]:
        return self._stacks
    
    @property
    def get_bar(self) -> Bar:
        return self._bar
    
    @property
    def get_home(self) -> Home:
        return self._home
    

# def test():
#     board = Board()
#     # print(board._stone_location)
#     # for stack in board.get_stacks:
#     print(board._stone_location)
#     some_stone = board._stacks[0].peek_piece()
#     board.move_stone(some_stone, 3)
#     print(board._stone_location)

# test()