import pygame as pg

import config
from game import Game


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
