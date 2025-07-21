# import BackgammonEngine
# import pygame as pg
# import os
# import BackgammonEngine
# from collections import deque

# # Domain Layer (Pure Game Logic)
#     # Stack - Manages piece storage/stacking rules
#     # Piece - Data-only model (color, position, etc.)
#     # Board - Manages all stacks and game rules

# # Presentation Layer (Display/Interaction)
#     # StackView - handles the 
#     # Renderer - Handles all Pygame drawing
#     # InputHandler - Processes mouse/keyboard events

# # Coordination Layer
#     # Game (Facade) - Mediates between layers

# pg.init()

# #Dimension
# HEIGHT_BOARD = 13
# WIDTH_BOARD = 15
# WIDTH = 1500
# HEIGHT = 800
# screen = pg.display.set_mode((WIDTH, HEIGHT))
# pg.display.set_caption("Backgammon")
# FPS = 30
# SQ_SIZE = HEIGHT // HEIGHT_BOARD
# BACKGROUNG = pg.image.load(os.path.join('images', 'plocha.jpg'))


# ###colors
# lite_brown = (250, 234, 177)
# color1 = (197, 137, 64)
# WHITE_COLUMN = (193, 193, 193)
# BLACK_COLUMN = (229, 186, 115)
# RED = (250, 0, 0)
# BLACK = (0, 0, 0)

# ###images
# dice1 = pg.image.load(os.path.join("images", "dice-six-faces-one.png"))
# dice2 = pg.image.load(os.path.join("images", "dice-six-faces-two.png"))
# dice3 = pg.image.load(os.path.join("images", "dice-six-faces-three.png"))
# dice4 = pg.image.load(os.path.join("images", "dice-six-faces-four.png"))
# dice5 = pg.image.load(os.path.join("images", "dice-six-faces-five.png"))
# dice6 = pg.image.load(os.path.join("images", "dice-six-faces-six.png"))
# wp = pg.image.load(os.path.join("images", "white_got.png"))
# bp = pg.image.load(os.path.join("images", "black_got.png"))




# ## Objevim kameny pomoci classu Stone
# ## Cerny kameny

# # black_piece1 = Stone("black")
# # black_piece2 = Stone("black")
# # black_piece3 = Stone("black")
# # black_piece4 = Stone("black")
# # black_piece5 = Stone("black")

# # black_piece6 = Stone("black")
# # black_piece7 = Stone("black")
# # black_piece8 = Stone("black")

# # black_piece9 = Stone("black")
# # black_piece10 = Stone("black")
# # black_piece11 = Stone("black")
# # black_piece12 = Stone("black")
# # black_piece13 = Stone("black")

# # black_piece14 = Stone("black")
# # black_piece15 = Stone("black")

# #bile kameny

# # white_piece1 = Stone("white")
# # white_piece2 = Stone("white")
# # white_piece3 = Stone("white")
# # white_piece4 = Stone("white")
# # white_piece5 = Stone("white")

# # white_piece6 = Stone("white")
# # white_piece7 = Stone("white")
# # white_piece8 = Stone("white")

# # white_piece9 = Stone("white")
# # white_piece10 = Stone("white")
# # white_piece11 = Stone("white")
# # white_piece12 = Stone("white")
# # white_piece13 = Stone("white")

# # white_piece14 = Stone("white")
# # white_piece15 = Stone("white")


    

# # stack1 = Stack(1, black_piece14, black_piece15)
# # stack2 = Stack(2, None)
# # stack3 = Stack(3, None)
# # stack4 = Stack(4, None)
# # stack5 = Stack(5, None)
# # stack6 = Stack(6, white_piece1, white_piece2, white_piece3, white_piece4, white_piece5)
# # stack7 = Stack(7, None)
# # stack8 = Stack(8, white_piece6, white_piece7, white_piece8)
# # stack9 = Stack(9, None)
# # stack10 = Stack(10, None)
# # stack11 = Stack(11, None)
# # stack12 = Stack(12, black_piece9, black_piece10, black_piece11, black_piece12, black_piece13)
# # stack13 = Stack(13, white_piece13, white_piece12, white_piece11, white_piece10, white_piece9)
# # stack14 = Stack(14, None)
# # stack15 = Stack(15, None)
# # stack16 = Stack(16, None)
# # stack17 = Stack(17, black_piece8, black_piece7, black_piece6)
# # stack18 = Stack(18, None)
# # stack19 = Stack(19, black_piece5, black_piece4, black_piece3, black_piece2, black_piece1)
# # stack20 = Stack(20, None)
# # stack21 = Stack(21, None)
# # stack22 = Stack(22, None)
# # stack23 = Stack(23, None)
# # stack24 = Stack(24, white_piece15, white_piece14)
# # print(stack1.elements)

# class MoveMediator:
#     # so i am thinking this will hanlges the stacks, checkers and bar
#     # as well as being a commnand pattern where i can do and undo

# class Board:
#     def __init__(self):


#     def draw_gameState(self, screen):
#         self._draw_board(screen)
#         # draw_pieces(screen, gs.board)


#     def _draw_board(self, screen):
#         color = WHITE_COLUMN
#         screen.fill(lite_brown)
#         for c in range(WIDTH_BOARD):
#             for r in range(HEIGHT_BOARD):
#                 #outline
#                 if r == 0 or c == 0 or c == WIDTH_BOARD-1 or r == HEIGHT_BOARD-1 or c == 7:
#                     pg.draw.rect(screen, color1, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
#                 #triangles
#                 elif r == 1:
#                     pg.draw.polygon(screen, color,
#                                 [(c * SQ_SIZE, r * SQ_SIZE), ((c + 1) * SQ_SIZE, r * SQ_SIZE),
#                                     (c * SQ_SIZE + 0.5 * SQ_SIZE, 6 * SQ_SIZE)])
#                     if color == WHITE_COLUMN:
#                         color = BLACK_COLUMN
#                     else:
#                         color = WHITE_COLUMN
#                 elif r == 11:
#                     pg.draw.polygon(screen, color,
#                                 [(c * SQ_SIZE, (r+1) * SQ_SIZE), ((c + 1) * SQ_SIZE, (r+1) * SQ_SIZE),
#                                     (c * SQ_SIZE + 0.5 * SQ_SIZE, 7 * SQ_SIZE)])
#                 #to test a grid
#                 #pg.draw.rect(screen, RED, pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)


#         pg.draw.line(screen, BLACK, (7.5*SQ_SIZE, 0), (7.5*SQ_SIZE, HEIGHT_BOARD*SQ_SIZE), 10)
#         pg.draw.rect(screen, RED, pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)
#         pg.display.flip()

#     def _draw_pieces(self): 
#         ...


# def main():
#     clock = pg.time.Clock()
#     run = True
#     game_board = Board()
#     while run:
#         gs = BackgammonEngine.Game_state()
#         clock.tick(FPS)

#         game_board.draw_gameState(screen)
#         # draw_pieces(screen, gs.board)

#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 run = False


#     pg.quit()





# if __name__ == '__main__':
#     main()



