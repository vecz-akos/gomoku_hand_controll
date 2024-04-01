#!/usr/bin/env python3

import pygame as pg

from gomoku import GomokuState, Sign
from view import GomokuGameView

def update_state(gomoku_state, view, position):
    x, y = position
    row, col = view.get_cell(x, y)
    try:
        new_state = gomoku_state.set_step(row, col)
    except:
        return gomoku_state
    return new_state

def main():
    pg.init()
    clock = pg.time.Clock()
    running = True

    board_size = 4

    gomoku_state = GomokuState(size=board_size)
    view = GomokuGameView(board_size=board_size)
    view.clear()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                gomoku_state = update_state(gomoku_state, view, pg.mouse.get_pos())

        view.draw_board()
        
        for i, row in enumerate(gomoku_state.board):
            for j, col in enumerate(row):
                if col is Sign.X:
                    view.draw_x(j, i)
                elif col is Sign.O:
                    view.draw_o(j, i)

        view.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
