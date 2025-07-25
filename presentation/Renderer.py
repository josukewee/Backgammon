import pygame as pg
from typing import List, Dict
from dataclasses import dataclass

class Renderer:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.assets = self._load_assets()
        self.animations: List[StoneAnimation] = []
        self.static_surface = None
        self.dirty = True

    def _load_assets(self) -> Dict[str, pg.Surface]:
        return {
            "white_stone": pg.Surface((30, 30), pg.SRCALPHA),
            "black_stone": pg.Surface((30, 30), pg.SRCALPHA),
            "board": pg.Surface((800, 600))
        }

    def on_board_change(self, change_type: str, *args) -> None:
        if change_type == "move":
            from_pos, to_pos = args
            self._start_animation(from_pos, to_pos)
        self.dirty = True

    def _start_animation(self, from_pos: int, to_pos: int) -> None:
        start_px = self._stack_to_pixels(from_pos)
        end_px = self._stack_to_pixels(to_pos)
        stone = self._get_stone_at_position(from_pos)
        self.animations.append(StoneAnimation(stone, start_px, end_px))

    def _stack_to_pixels(self, stack_id: int) -> tuple[int, int]:
        col = stack_id % 12
        row = 0 if stack_id < 12 else 1
        x = col * SQ_SIZE + SQ_SIZE // 2
        y = (row * 11 + 1) * SQ_SIZE if row == 0 else (row * 11) * SQ_SIZE
        return (x, y)

    def update(self, dt: float) -> None:
        self._update_animations(dt)
        if self.dirty or self.animations:
            self._redraw()

    def _update_animations(self, dt: float) -> None:
        for anim in self.animations[:]:
            if anim.update(dt):
                self.animations.remove(anim)
                self.dirty = True

    def _redraw(self) -> None:
        if self.dirty:
            self._draw_static_elements()
            self.dirty = False
        
        self.screen.blit(self.static_surface, (0, 0))
        self._draw_animations()
        pg.display.flip()

    def _draw_static_elements(self) -> None:
        self.static_surface = pg.Surface((800, 600), pg.SRCALPHA)
        self._draw_board(self.static_surface)
        self._draw_stones(self.static_surface)

    def _draw_board(self, surface: pg.Surface) -> None:
        surface.fill(lite_brown)
        for c in range(WIDTH_BOARD):
            for r in range(HEIGHT_BOARD):
                if r == 0 or c == 0 or c == WIDTH_BOARD-1 or r == HEIGHT_BOARD-1 or c == 7:
                    pg.draw.rect(surface, color1, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                elif r == 1:
                    color = WHITE_COLUMN if c % 2 == 0 else BLACK_COLUMN
                    pg.draw.polygon(surface, color, [
                        (c * SQ_SIZE, r * SQ_SIZE),
                        ((c + 1) * SQ_SIZE, r * SQ_SIZE),
                        (c * SQ_SIZE + 0.5 * SQ_SIZE, 6 * SQ_SIZE)
                    ])
                elif r == 11:
                    color = WHITE_COLUMN if c % 2 == 1 else BLACK_COLUMN
                    pg.draw.polygon(surface, color, [
                        (c * SQ_SIZE, (r+1) * SQ_SIZE),
                        ((c + 1) * SQ_SIZE, (r+1) * SQ_SIZE),
                        (c * SQ_SIZE + 0.5 * SQ_SIZE, 7 * SQ_SIZE)
                    ])

        pg.draw.line(surface, BLACK, (7.5*SQ_SIZE, 0), (7.5*SQ_SIZE, HEIGHT_BOARD*SQ_SIZE), 10)

    def _draw_stones(self, surface: pg.Surface) -> None:
        for stack_id in range(24):
            stack = self._get_stack(stack_id)
            for i, stone in enumerate(stack.get_stones()):
                if not self._is_animating(stone):
                    pos = self._stack_to_pixels(stack_id)
                    pos = (pos[0], pos[1] - i * STONE_SPACING)
                    surface.blit(self.assets[f"{stone.color}_stone"], pos)

    def _draw_animations(self) -> None:
        for anim in self.animations:
            pos = anim.get_current_pos()
            self.screen.blit(self.assets[f"{anim.stone.color}_stone"], pos)

    def _is_animating(self, stone: object) -> bool:
        return any(anim.stone == stone for anim in self.animations)