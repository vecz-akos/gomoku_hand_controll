#!/usr/bin/env python3

import pygame as pg
import os

from gomoku import GomokuState, Sign
from tracker import Tracker
from view import GomokuGameView

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (700,30)

TRACKER_UPDATE_EVENT = pg.USEREVENT + 1

def update_state_by_click(gomoku_state, view, position):
    x, y = position
    row, col = view.get_cell(x, y)
    try:
        new_state = gomoku_state.set_step(row, col)
    except:
        return gomoku_state
    return new_state

def update_state(gomoku_state, cell):
    try:
        new_state = gomoku_state.set_step(*cell)
    except:
        return gomoku_state
    return new_state

def main():
    pg.init()
    clock = pg.time.Clock()
    running = True
    pg.time.set_timer(TRACKER_UPDATE_EVENT, 100)

    board_size = 3

    gomoku_state = GomokuState(size=board_size)
    view = GomokuGameView(board_size=board_size)
    view.clear()
    tracker = Tracker()
    tracker.update()
    last_cells = []
    selected_cell = (-1, -1)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_ESCAPE, pg.K_q]:
                    running = False
                elif event.key == pg.K_SPACE:
                    tracker.capture_template(True)
            elif event.type == pg.MOUSEBUTTONDOWN:
                gomoku_state = update_state_by_click(gomoku_state, view, pg.mouse.get_pos())
            elif event.type == TRACKER_UPDATE_EVENT and tracker.is_template_captured:
                tracker.update()
                current_cell = view.get_cell_from_range(tracker.current_pos[0], tracker.current_pos[1])
                last_cells = [view.get_cell_from_range(p[0], p[1]) for p in tracker.prev_pos]
                if (all([current_cell == cell for cell in last_cells])) and current_cell != (-1, -1):
                    selected_cell = current_cell
                elif selected_cell == (-1, -1) and all([last_cells[3] == cell and cell != (-1, -1) for cell in last_cells[3:]]):
                    gomoku_state = update_state(gomoku_state, last_cells[3])
                    selected_cell = (-1, -1)
                else:
                    selected_cell = (-1, -1)
        
        view.clear()
        if tracker.is_template_captured:
            view.draw_marker(tracker.current_pos[0], tracker.current_pos[1])
            if selected_cell != [-1, -1]:
                view.select_cell(*selected_cell)
        else:
            tracker.capture_template()

        view.draw_board()
        
        for i, row in enumerate(gomoku_state.board):
            for j, col in enumerate(row):
                if col is Sign.X:
                    view.draw_x(j, i)
                elif col is Sign.O:
                    view.draw_o(j, i)
        
        if (winner := gomoku_state.get_winner()) is not Sign.EMPTY:
            view.draw_message(f"Winner: {'X' if winner is Sign.X else 'O'}")

        view.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
