import pygame as pg
from typing import Optional, Tuple

from core import eventHandler
from presentation.Renderer import Renderer

class InputHandler:
    def __init__(self, renderer: Renderer, eventHandler: eventHandler):
        self.renderer = renderer
        self.selected_stack: Optional[int] = None
        self.eventHandler = eventHandler

        self._selected_stack = None

    def process_events(self) -> bool:
        """Process all pygame events. Returns False if the game should quit."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                stack_id = self.renderer.get_stack_from_pos(event.pos)
                if stack_id:
                    print(stack_id)
                    self._selected_stack = stack_id
                    self.renderer.highlight_stack(stack_id)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Roll dice with SPACE
                    self.mediator.roll_dice()
            
        return True

    def _handle_click(self, stack_id: int) -> None:
        """Handle clicking on a stack."""
        if self.selected_stack is None:
            # First click → select a stack if it has a valid stone
            if self.mediator.can_select_stack(stack_id):
                self.selected_stack = stack_id
        else:
            # Second click → try to move from selected_stack to stack_id
            moved = self.mediator.try_move(self.selected_stack, stack_id)
            if moved:
                self.renderer.on_board_change("move", self.selected_stack, stack_id)
            self.selected_stack = None
            self.renderer.clear_highlights()




