# everything below is displaying logic doesn't belong in here 
    def draw_gameState(self, screen):
        self._draw_board(screen)
        # draw_pieces(screen, gs.board)


    def _draw_board(self, screen):
        color = WHITE_COLUMN
        screen.fill(lite_brown)
        for c in range(WIDTH_BOARD):
            for r in range(HEIGHT_BOARD):
                #outline
                if r == 0 or c == 0 or c == WIDTH_BOARD-1 or r == HEIGHT_BOARD-1 or c == 7:
                    pg.draw.rect(screen, color1, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                #triangles
                elif r == 1:
                    pg.draw.polygon(screen, color,
                                [(c * SQ_SIZE, r * SQ_SIZE), ((c + 1) * SQ_SIZE, r * SQ_SIZE),
                                    (c * SQ_SIZE + 0.5 * SQ_SIZE, 6 * SQ_SIZE)])
                    if color == WHITE_COLUMN:
                        color = BLACK_COLUMN
                    else:
                        color = WHITE_COLUMN
                elif r == 11:
                    pg.draw.polygon(screen, color,
                                [(c * SQ_SIZE, (r+1) * SQ_SIZE), ((c + 1) * SQ_SIZE, (r+1) * SQ_SIZE),
                                    (c * SQ_SIZE + 0.5 * SQ_SIZE, 7 * SQ_SIZE)])
                #to test a grid
                #pg.draw.rect(screen, RED, pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)


        pg.draw.line(screen, BLACK, (7.5*SQ_SIZE, 0), (7.5*SQ_SIZE, HEIGHT_BOARD*SQ_SIZE), 10)
        pg.draw.rect(screen, RED, pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)
        pg.display.flip()