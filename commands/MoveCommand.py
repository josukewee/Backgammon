from typing import Optional, Union
from commands.command import Command
from datastructures.Bar import Bar
from datastructures.Stone import Stone
from core.moveMediator import MoveMediator


class MoveCommand(Command):

    def __init__(self, mediator: MoveMediator, from_stack: Union[int, Bar], to_stack: int):
        self._mediator = mediator
        self.from_stack = from_stack
        self.to_stack = to_stack

        self._moved_stone: Optional[Stone] = None
        self._hit_stone: Optional[Stone] = None
        
        self._origin_container: Optional[Union[int, Bar]] = None 
        self._destination_container: Optional[Union[int, Bar]] = None
        # track which die value was actually consumed for this move
        self._consumed_die_value: Optional[int] = None

    def execute(self):
        self._origin_container = self.from_stack

        self._moved_stone, self._hit_stone = self._mediator.execute_move(self.from_stack, self.to_stack)

        board = self._mediator._board
        loc = board.get_stone_location(self._moved_stone)
        self._destination_container = loc

    def undo(self):
        if not self._moved_stone:
            raise RuntimeError("Cannot undo before execute")

        board = self._mediator._board

        # source of the reverse move
        from_container = board.get_stone_location(self._moved_stone)

        # destination of the reverse move
        to_container = self._origin_container

        self._mediator.move_stone(self._moved_stone, from_container, to_container)

        if self._hit_stone is not None:
            # The point that was captured is the destination stack index of the original move
            if isinstance(self.to_stack, int) and 1 <= self.to_stack <= 24:
                self._mediator.move_stone(self._hit_stone, self._mediator._board.get_bar, self.to_stack)

    # dice bookkeeping interfaces
    def set_consumed_die_value(self, value: int) -> None:
        self._consumed_die_value = value

    def get_consumed_die_value(self) -> Optional[int]:
        return self._consumed_die_value


    