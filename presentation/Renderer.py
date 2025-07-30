import os
from datastructures.Board import Board
from datastructures.Stone import Stone


from presentation.StoneAnimation import StoneAnimation
import pygame as pg
from typing import List, Dict, Union
from dataclasses import dataclass

class Renderer:

    # #Dimension
    HEIGHT_BOARD = 13
    WIDTH_BOARD = 15
    WIDTH = 1500
    HEIGHT = 800
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Backgammon")
    FPS = 30
    SQ_SIZE = HEIGHT // HEIGHT_BOARD
    # BACKGROUNG = pg.image.load(os.path.join('images', 'plocha.jpg'))


    ###colors
    LITE_BROWN = (250, 234, 177)
    COLOR1 = (197, 137, 64)
    WHITE_COLUMN = (193, 193, 193)
    BLACK_COLUMN = (229, 186, 115)
    RED = (250, 0, 0)
    BLACK = (0, 0, 0)

    def __init__(self, screen_width: int = WIDTH, screen_height: int = HEIGHT):
        # for testing only
        self.board = Board()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.assets = self._load_assets()
        self.animations: List[StoneAnimation] = []
        self.static_surface = None
        self.dirty = True
        self.font = pg.font.SysFont("Arial", 20)  # You can pick size and font
        self.text_color = (0, 0, 0)

        # might not be the place to be
        pg.font.init()
        self.my_font = pg.font.SysFont('Comic Sans MS', 30)

    def _load_assets(self) -> Dict[str, pg.Surface]:
        return {
            "white_stone": self._load_image("white_got.png"),
            "black_stone": self._load_image("black_got.png"),
            "white_highligh": self._load_image("white_highlight.png"),
            "white_highligh": self._load_image("black_highlight.png"),
            "board": pg.Surface((800, 600))

        }
    

    def _load_image(self, filename: str):
        """Loads the filenamblack_highlighte image from the assets folder"""

        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(current_dir)

        try:
            image = pg.image.load(os.path.join(project_root, "assets", "images", filename)).convert_alpha()
            return image

        except pg.error as e:
            print("Error occured", e)
            
    def init(self):
        # Initialize static_surface (if not done already)
        if self.static_surface is None:
            self.static_surface = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)
        
        # Draw everything to the buffer
        self._draw_board(self.static_surface)
        self._draw_stones(self.static_surface)
        
        # Blit to screen
        self.screen.blit(self.static_surface, (0, 0))
        pg.display.flip()

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

    def highlight_stack(self, stack_id: int):
        position = self._stack_to_pixels(stack_id)

    def get_stack_from_pos(self, pos: tuple[int, int]) -> Union[int, None]:
        for stack_id in range(1, 25):
            if self._stack_rect(stack_id).collidepoint(pos):
                return stack_id
        return None

    def _stack_rect(self, stack_id: int) -> pg.Rect:
        """Return the rectangle area on the screen that corresponds to a stack."""

        center_x, center_y = self._stack_to_pixels(stack_id)

        width = self.SQ_SIZE 
        height = self.SQ_SIZE * 5 
        
        x = center_x - width // 2
        if stack_id <= 12:  
            y = center_y - height
        else:               
            y = center_y - self.SQ_SIZE

        return pg.Rect(x+self.SQ_SIZE//2, y+self.SQ_SIZE, width, height)
    
    def debug_draw_stack_rects(self) -> None:
        font = pg.font.SysFont("Arial", 18)

        for stack_id in range(1, 25):
            rect = self._stack_rect(stack_id)

            # green rect outline
            pg.draw.rect(self.screen, (0, 255, 0), rect, 2)

            # draw stack number
            text_surface = font.render(str(stack_id), True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

            # for debugging console
            print(f"Stack {stack_id}: {rect}")
        
    def _stack_to_pixels(self, stack_id: int) -> tuple[int, int]:
        """
        Map a stack_id (0–23) to board grid coordinates, then to pixel center.
        Stack 0 = bottom right, numbering counterclockwise.
        """

        # work with 1-based indexing for clarity
        stack_num = stack_id + 1

        # bottom half: stacks 1–12 (right to left)
        if 1 <= stack_num <= 13:
            col = 14 - stack_num
            if stack_num > 7:
                col -= 1  # skip over bar
            x = (col + 1) * self.SQ_SIZE
            y = (self.HEIGHT_BOARD - 2) * self.SQ_SIZE

        # top half: stacks 13–24 (left to right)
        else:
            col = stack_num - 14
            if stack_num >= 20:
                col += 1  # skip over bar
            x = (col + 1) * self.SQ_SIZE
            y = 1 * self.SQ_SIZE

        return int(x), int(y)



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

        
    def _draw_board(self, screen):
        color = self.WHITE_COLUMN
        screen.fill(self.LITE_BROWN)
        for c in range(self.WIDTH_BOARD):
            for r in range(self.HEIGHT_BOARD):
                #outline
                if r == 0 or c == 0 or c == self.WIDTH_BOARD-1 or r == self.HEIGHT_BOARD-1 or c == 7:
                    pg.draw.rect(screen, self.COLOR1, pg.Rect(c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
                #triangles
                elif r == 1:
                    pg.draw.polygon(screen, color,
                                [(c * self.SQ_SIZE, r * self.SQ_SIZE), ((c + 1) * self.SQ_SIZE, r * self.SQ_SIZE),
                                    (c * self.SQ_SIZE + 0.5 * self.SQ_SIZE, 6 * self.SQ_SIZE)])
                    if color == self.WHITE_COLUMN:
                        color = self.BLACK_COLUMN
                    else:
                        color = self.WHITE_COLUMN
                elif r == 11:
                    pg.draw.polygon(screen, color,
                                [(c * self.SQ_SIZE, (r+1) * self.SQ_SIZE), ((c + 1) * self.SQ_SIZE, (r+1) * self.SQ_SIZE),
                                    (c * self.SQ_SIZE + 0.5 * self.SQ_SIZE, 7 * self.SQ_SIZE)])
                #to test a grid
                # pg.draw.rect(screen, self.RED, pg.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE), 2)


        pg.draw.line(screen, self.BLACK, (7.5*self.SQ_SIZE, 0), (7.5*self.SQ_SIZE, self.HEIGHT_BOARD*self.SQ_SIZE), 10)
        pg.draw.rect(screen, self.RED, pg.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE), 2)
        pg.display.flip()

    def _draw_stones(self, surface: pg.Surface) -> None:
        for stack_id in range(1, 25):
            stack = self.board.get_stack(stack_id)
            for i, stone in enumerate(stack.get_stones):
                color = stone.get_color
                if not self._is_animating(stone):
                    base_x, base_y = self._stack_to_pixels(stack_id)

                    # Bottom half (1–12): stack upwards
                    if 1 <= stack_id <= 12:
                        pos = (base_x, base_y - i * self.SQ_SIZE)
                    # Top half (13–24): stack downwards
                    else:
                        pos = (base_x, base_y + i * self.SQ_SIZE)

                    surface.blit(self.assets[f"{color}_stone"], pos)

    def _draw_animations(self) -> None:
        for anim in self.animations:
            pos = anim.get_current_pos()
            self.screen.blit(self.assets[f"{anim.stone.color}_stone"], pos)

    def _is_animating(self, stone: object) -> bool:
        return any(anim.stone == stone for anim in self.animations)
    
def test():
    renderer_test = Renderer()
        # Initialize
    pg.init()
    renderer = Renderer()
    clock = pg.time.Clock()
    
    # Force-draw one white stone at position 1 (for testing)
    renderer.board.get_stack(1).add_stone("white")  # Mock a stone
    
    # Main loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        # Update and render
        renderer.update(1/60)  # Fixed delta time
        
        # Limit FPS (optional)
        clock.tick(60)
    
    pg.quit()