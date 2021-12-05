import pygame as pg

import config
from game import Game
from logics_TMP import get_const_4_cell


class Interface(Game):
    def __init__(self):
        super().__init__(config.CAPTION, config.WIDTH, config.HEIGHT, config.ICON, config.FRAMERATE)
        self.blocks = config.BLOCKS
        self.size_block = config.SIZE_BLOCK
        self.margin = config.MARGIN
        self.generalFont = config.GENERAL_FONT

    def draw_main(self):
        """Draws the main interface"""
        self.screen.blit(pg.transform.scale(pg.image.load("images\\BG\\BG.jpg"), (self.width, self.height + 2)), (0, 0))
        self.screen.blit(pg.transform.scale(pg.image.load("images\\elements\\around_arrow.png"), (43, 43)), (453, 159))
        self.screen.blit(pg.transform.scale(pg.image.load("images\\elements\\arrow.png"), (58, 58)), (374, 154))
        self.screen.blit(pg.transform.scale(pg.image.load("images\\elements\\home.png"), (38, 38)), (314, 162))

        for row in range(self.blocks):  # Building cells
            for column in range(self.blocks):
                value, font = get_const_4_cell(self.board[row][column], self.generalFont)
                text = font.render(f'{value}', True, '#545E66' if value in (2, 4) else '#ebeeff')  # GRAY or WHITE
                w = column * self.size_block + (column - 1) * self.margin + 30
                h = row * self.size_block + (row - 1) * self.margin + 240
                if value != 0:  # Placing numbers on cells
                    pg.draw.rect(self.screen, config.COLORS[value],
                                     (w, h, self.size_block + 2, self.size_block + 2), border_radius=7)
                    font_w, font_h = text.get_size()
                    text_x = w + (self.size_block - font_w) / 2
                    text_y = h + (self.size_block - font_h) / 2 - 6
                    self.screen.blit(text, (text_x, text_y))
