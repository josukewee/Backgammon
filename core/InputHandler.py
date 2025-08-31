import pygame as pg
from typing import Optional
from core.eventHandler import eventHandler
from presentation.Renderer import Renderer


class InputHandler:
    """
    Captures user input (mouse, keyboard), converts it into
    high-level game events, and sends them to the event queue.
    """

    def __init__(self, renderer: Renderer, events: eventHandler) -> None:
        self.renderer = renderer
        self.events = events
        self._selected_stack: Optional[int] = None

    def process_events(self) -> bool:
        """
        Process all Pygame events for this frame.
        Returns False if the game should quit.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.events.append({"type": "QuitEvent"})
                return False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._clear_selection()
                elif event.key == pg.K_r:
                    # Player requests dice roll (optional if you want manual rolling)
                    self.events.append({"type": "RollDiceRequest"})

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self._handle_left_click(event.pos)
                elif event.button == 3:  # Right click
                    self._clear_selection()

        return True

    # -------------------------
    # Internal helpers
    # -------------------------
    def _handle_left_click(self, pos: tuple[int, int]) -> None:
        stack_id = self.renderer.get_stack_from_pos(pos)
        if stack_id is None:
            self._clear_selection()
            return

        if self._selected_stack is None:
            # First click: Check if this stack has movable stones for current player
            if self._can_select_stack(stack_id):
                self._selected_stack = stack_id
                # Request possible destinations from GameEngine
                self.events.append({
                    "type": "StackSelected",
                    "stack_id": stack_id
                })
            else:
                # Invalid selection → clear
                self._clear_selection()
        else:
            # Second click: Attempt to move
            if stack_id != self._selected_stack:
                self.events.append({
                    "type": "MoveEvent",
                    "from_stack": self._selected_stack,
                    "to_stack": stack_id
                })
            self._clear_selection()


    def _can_select_stack(self, stack_id: int) -> bool:
        # For now, just allow all selections (GameEngine will reject invalid moves)
        return True

    def _clear_selection(self) -> None:
        self._selected_stack = None
        # self.renderer.clear_highlight()
