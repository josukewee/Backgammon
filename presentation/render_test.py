import pygame as pg
from datastructures.Stone import Stone
from presentation.Renderer import Renderer
from datastructures.Stack import Stack


def main():
    # stack = Stack(1, Stone(1, "white"), Stone(2, "black"))
    # print(stack.get_stones)
    # Initialize
    pg.init()
    renderer = Renderer()
    clock = pg.time.Clock()
    
    # Force-draw one white stone at position 1 (for testing)
     # Mock a stone
    renderer.init()
    renderer.debug_draw_stack_rects()
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

if __name__ == "__main__":
    main()