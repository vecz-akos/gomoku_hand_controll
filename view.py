#!/usr/bin/env python3

import pygame as pg

class GomokuGameView:
    def __init__(self, board_size=3):
        screen_width = 800
        screen_height = 600
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.board_size = board_size
        self.margin = (50, 100)
        self.cell_width = 100
        
        pg.display.set_caption("Gomoku")
    
    def flip(self):
        pg.display.flip()
    
    def clear(self):
        self.screen.fill("white")

    def draw_board(self):
        for i in range(self.board_size+1):
            pg.draw.line(self.screen, "black", (self.margin[0] + i*self.cell_width, self.margin[1]), (self.margin[0] + i*self.cell_width, self.margin[1] + self.board_size*self.cell_width), 3)
        for i in range(self.board_size+1):
            pg.draw.line(self.screen, "black", (self.margin[0], self.margin[1] + i*self.cell_width), (self.margin[0] + self.board_size*self.cell_width, self.margin[1] + i*self.cell_width), 3)
    
    def draw_x(self, col, row):
        inner_margin = 25
        pg.draw.line(self.screen, "black", (self.margin[0] + col*self.cell_width + inner_margin, self.margin[1] + row*self.cell_width + inner_margin), (self.margin[0] + (col+1)*self.cell_width - inner_margin, self.margin[1] + (row+1)*self.cell_width - inner_margin), 3)
        pg.draw.line(self.screen, "black", (self.margin[0] + (col+1)*self.cell_width - inner_margin, self.margin[1] + row*self.cell_width + inner_margin), (self.margin[0] + col*self.cell_width + inner_margin, self.margin[1] + (row+1)*self.cell_width - inner_margin), 3)

    def draw_o(self, col, row):
        pg.draw.circle(self.screen, "black", (self.margin[0] + (col+.5)*self.cell_width, self.margin[1] + (row+.5)*self.cell_width), self.cell_width*.25, 3)
    
    def get_cell(self, x, y):
        col = (x-self.margin[0]) // self.cell_width
        row = (y-self.margin[1]) // self.cell_width
        return row, col
