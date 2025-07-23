from typing import Optional, Union
from commands.command import Command
from datastructures.Bar import Bar
from datastructures.Stone import Stone
from datastructures.moveMediator import MoveMediator


class MoveCommand(Command):

    def __init__(self, mediator: MoveMediator, from_stack: Union[int, Bar], to_stack: int):
        self._mediator = mediator
        self.from_stack = from_stack
        self.to_stack = to_stack

        self._moved_stone: Optional[Stone] = None
        self._hit_stone: Optional[Stone] = None
        self._used_die: Optional[int] = None

    def execute(self):
        self._moved_stone, self._hit_stone = self._mediator.execute_move(self.from_stack, self.to_stack)

    def undo(self):
         # still thinking of way to handle the undoing command and wher should i put the logic
        self._mediator.move_stone(self._moved_stone, self.to_stack, self.from_stack)

        # Restore hit stone if any
        if self.hit_stone:
            self._mediator.move_stone(self._hit_stone, self._mediator._board.get_bar, self.to_stack)


    