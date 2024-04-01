#!/usr/bin/env python3

import pygame as pg

from gomoku import GomokuState, Sign
    
CELL_WIDTH = 100
MARGIN = 50

def update_state(gomoku_state, position):
    x, y = position
    col = (x-MARGIN) // CELL_WIDTH
    row = (y-MARGIN) // CELL_WIDTH
    try:
        new_state = gomoku_state.set_step(row, col)
    except:
        return gomoku_state
    return new_state

def draw_x(screen, x, y):
    inner_margin = 25
    pg.draw.line(screen, "black", (MARGIN + x*CELL_WIDTH + inner_margin, MARGIN + y*CELL_WIDTH + inner_margin), (MARGIN + (x+1)*CELL_WIDTH - inner_margin, MARGIN + (y+1)*CELL_WIDTH - inner_margin), 3)
    pg.draw.line(screen, "black", (MARGIN + (x+1)*CELL_WIDTH - inner_margin, MARGIN + y*CELL_WIDTH + inner_margin), (MARGIN + x*CELL_WIDTH + inner_margin, MARGIN + (y+1)*CELL_WIDTH - inner_margin), 3)

def draw_o(screen, x, y):
    pg.draw.circle(screen, "black", (MARGIN + (x+.5)*CELL_WIDTH, MARGIN + (y+.5)*CELL_WIDTH), CELL_WIDTH*.25, 3)

def main():
    pg.init()

    screen_width = 800
    screen_height = 600
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Gomoku")
    clock = pg.time.Clock()
    running = True

    board_size = 4

    gomoku_state = GomokuState(size=board_size)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                gomoku_state = update_state(gomoku_state, pg.mouse.get_pos())

        screen.fill("white")
        for i in range(board_size+1):
            pg.draw.line(screen, "black", (MARGIN + i*CELL_WIDTH, MARGIN), (MARGIN + i*CELL_WIDTH, MARGIN + board_size*CELL_WIDTH), 3)
        for i in range(board_size+1):
            pg.draw.line(screen, "black", (MARGIN, MARGIN + i*CELL_WIDTH), (MARGIN + board_size*CELL_WIDTH, MARGIN + i*CELL_WIDTH), 3)
        
        for i, row in enumerate(gomoku_state.board):
            for j, col in enumerate(row):
                if col is Sign.X:
                    draw_x(screen, j, i)
                elif col is Sign.O:
                    draw_o(screen, j, i)

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
