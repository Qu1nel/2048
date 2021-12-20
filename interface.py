import pygame as pg

import config
import database
from game import Game
from logics_TMP import get_const_4_cell, get_size_font


class Interface(Game):
    def __init__(self):
        super().__init__(config.CAPTION, config.WIDTH, config.HEIGHT, config.ICON, config.FRAMERATE)
        self.blocks = config.BLOCKS
        self.size_block = config.SIZE_BLOCK
        self.margin = config.MARGIN
        self.generalFont = config.GENERAL_FONT
        self.adjustment = lambda x, y: len(str(abs(y))) * 8 if x == 25 else len(str(abs(y))) * 7
        self.delta = 0

    def draw_victory(self):
        if not self.victory:
            blur = pg.Surface((self.width, self.height), pg.SRCALPHA)
            blur.fill((0, 0, 0, 85))
            self.screen.blit(blur, (0, 0))

            font_H1 = pg.font.Font(self.generalFont, 90)
            text_H1 = font_H1.render('You Win!', True, config.COLORS['WHITE'])
            self.screen.blit(text_H1, (self.width // 2 - text_H1.get_size()[0] // 2, 330))
            font_H3 = pg.font.Font(self.generalFont, 35)
            text_H3 = font_H3.render('Click any button to Continue', True, config.COLORS['WHITE'])
            self.screen.blit(text_H3, (self.width // 2 - text_H3.get_size()[0] // 2, 455))

            pg.display.update()

            running = True
            while running:
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.update()
                        running = False
                    if event.type == pg.KEYDOWN:
                        self.update()
                        running = False

            self.victory = True

    def draw_main(self):
        """Draws the main interface"""
        self.screen.blit(pg.transform.scale(pg.image.load("images\\BG\\BG.jpg"), (self.width, self.height + 2)), (0, 0))
        self.screen.blit(pg.transform.scale(pg.image.load("images\\elements\\around_arrow.png"), (43, 43)), (453, 159))
        self.screen.blit(pg.transform.scale(pg.image.load("images\\elements\\arrow.png"), (58, 58)), (374, 154))
        self.screen.blit(pg.transform.scale(pg.image.load("images\\elements\\home.png"), (38, 38)), (314, 162))

        self.screen.blit(
            pg.font.Font(self.generalFont, 17).render('HIGH SCORE', True, config.COLORS['GRAY']), (402, 55))
        self.screen.blit(pg.font.Font(self.generalFont, 18).render('SCORE', True, config.COLORS['GRAY']), (300, 55))
        self.screen.blit(pg.font.Font(self.generalFont, 86).render('2048', True, config.COLORS['WHITE']), (30, 2))

        best_score = database.get_best(1)['score']
        high_score = 0 if best_score == -1 else best_score
        size_score, size_high_score = get_size_font(self.score, high_score)  # Variable size of the font

        correct = self.adjustment(size_score, self.score)  # substitution for number score
        self.screen.blit(pg.font.Font(
            self.generalFont, size_score).render(f'{self.score}', True, config.COLORS['WHITE']), (325 - correct, 77))

        correct = self.adjustment(size_high_score, high_score)  # substitution for number high score
        self.screen.blit(
            pg.font.Font(self.generalFont, size_high_score).render(f'{high_score}', True, config.COLORS['WHITE']),
            (440 - correct, 77))

        if self.delta > 0:
            correct = len(str(abs(self.delta))) * 14  # substitution for number delta
            self.screen.blit(
                pg.font.Font(self.generalFont, 34).render(f'+{self.delta}', True, config.COLORS['WHITE']),
                (115 - correct, 160))

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
