import pygame as pg
from typing import Optional
from core.eventHandler import eventHandler
from presentation.Renderer import Renderer


class InputHandler:
    def __init__(self, renderer: Renderer, events: eventHandler) -> None:
        self.renderer = renderer
        self.events = events

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
                    self.events.append({"type": "ResetSelection"})
                elif event.key == pg.K_r:
                    self.events.append({"type": "RollDiceRequest"})
                elif event.key == pg.K_z and (pg.key.get_mods() & pg.KMOD_CTRL):
                    self.events.append({"type": "UndoRequest"})
                elif event.key == pg.K_y and (pg.key.get_mods() & pg.KMOD_CTRL):
                    self.events.append({"type": "RedoRequest"})

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  
                self._handle_left_click(event.pos)

        return True

    def _handle_left_click(self, pos: tuple[int, int]) -> None:
        """Convert a click position into a ClickStack or UI event (if valid)."""
        # Buttons first
        btn = self.renderer.get_button_from_pos(pos)
        if btn == "UNDO":
            self.events.append({"type": "UndoRequest"})
            return
        if btn == "REDO":
            self.events.append({"type": "RedoRequest"})
            return

        # Board stacks
        stack_id = self.renderer.get_stack_from_pos(pos)
        if stack_id is not None:
            self.events.append({
                "type": "ClickStack",
                "stack_id": stack_id
            })
