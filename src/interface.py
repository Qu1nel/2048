import sys
from abc import abstractmethod

import pygame as pg

import config
import database
from game import Game
from logics import get_const_4_cell, get_size_font


class Interface(Game):

    def __init__(self):
        super().__init__(config.CAPTION, config.WIDTH, config.HEIGHT, config.ICON, config.FRAMERATE)
        self.blocks = config.BLOCKS
        self.size_block = config.SIZE_BLOCK
        self.margin = config.MARGIN
        self.generalFont = config.GENERAL_FONT
        self.adjustment = lambda x, y: len(str(abs(y))) * 8 if x == 25 else len(str(abs(y))) * 7
        self.delta = 0

    def draw_game_over(self):
        repeat_box = pg.Rect(447, 153, 58, 58)

        blur = pg.Surface((self.width, self.height), pg.SRCALPHA)
        blur.fill((0, 0, 0, 60))
        self.screen.blit(blur, (0, 0))

        self.screen.blit(pg.font.Font(
            self.generalFont, 60).render('Game Over!', True, config.COLORS['WHITE']), (100, 290))
        pg.draw.rect(self.screen, '#8d8d8d', repeat_box, border_radius=8)
        round_arrow = pg.image.load("images/elements/around_arrow.png")
        self.screen.blit(pg.transform.scale(round_arrow, (43, 43)), (453, 159))
        pg.display.update()

        database.insert_result(self.username, self.score)
        make_decision = False
        while not make_decision:
            for event in pg.event.get():
                if event.type == pg.QUIT:  # Clicked on the cross
                    self.username = None
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.username = None
                        pg.quit()
                        sys.exit()
                    elif event.key == pg.K_RETURN:
                        self.username = None
                        make_decision = True
                    elif event.key == pg.K_BACKSPACE:
                        make_decision = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if repeat_box.collidepoint(event.pos):
                        make_decision = True

    def draw_top_gamers(self):
        menu_box = pg.Rect(225, 532, 75, 75)
        ALL_PLAYERS = database.get_best()

        backGround_with_crown = "images/BG/rating.jpg"
        backGround_without_crown = "images/BG/rating_nothing.jpg"
        path_bg = backGround_with_crown if database.get_best(1)['name'] is not None else backGround_without_crown
        rating_bg = pg.image.load(path_bg)
        menu = pg.image.load("images/elements/home.png")
        self.screen.blit(rating_bg, (0, 0))
        self.screen.blit(pg.transform.scale(menu, (50, 50)), (236, 543))

        self.screen.blit(pg.font.Font(self.generalFont, 120).render('Rating', True, config.COLORS['WHITE']), (86, -50))

        for id, player in ALL_PLAYERS.items():
            if player['name'] is None:
                self.screen.blit(pg.font.Font(
                    self.generalFont, 45).render('Nothing', True, config.COLORS['WHITE']), (180, 115 + 100 * id))
            else:
                name = pg.font.Font(self.generalFont, 40).render(player['name'] + ':', True, config.COLORS['WHITE'])
                if name.get_width() > 154:
                    S = player['name'] + ':'
                    self.screen.blit(pg.font.Font(
                        self.generalFont, 28).render(S, True, config.COLORS['WHITE']), (117, 135 + 100 * id))
                    size_font = 35
                    score_txt = pg.font.Font(
                        self.generalFont, size_font).render(str(player['score']), True, config.COLORS['WHITE'])
                    while 289 - name.get_width() + 20 + score_txt.get_width() - 117 > 309:
                        score_txt = pg.font.Font(
                            self.generalFont, size_font).render(str(player['score']), True, config.COLORS['WHITE'])
                        size_font -= 2
                    y = 128 if size_font == 35 else 133
                    x = pg.font.Font(self.generalFont, 28).render(player['name'] + ':',
                                                                  True, config.COLORS['WHITE']).get_width() + 127
                    direct_x = (406 - x) // 2 - score_txt.get_width() // 2
                else:
                    self.screen.blit(name, (117, 124 + 100 * id))
                    size_font = 35
                    score_txt = pg.font.Font(self.generalFont, size_font).render(str(player['score']),
                                                                                 True, config.COLORS['WHITE'])
                    while 289 - name.get_width() + 20 + score_txt.get_width() - 117 > 309:
                        score_txt = pg.font.Font(self.generalFont, size_font).render(str(player['score']),
                                                                                     True, config.COLORS['WHITE'])
                        size_font -= 2
                    y = 128 if size_font == 35 else 133
                    x = name.get_width() + 127
                    direct_x = (406 - x) // 2 - score_txt.get_width() // 2

                self.screen.blit(score_txt, (x + direct_x, y + 100 * id))

        pg.display.update()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    elif event.key == pg.K_BACKSPACE:
                        self.draw_menu()
                        return None
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if menu_box.collidepoint(event.pos):
                        self.draw_menu()
                        return None

    def draw_menu(self):
        play_box = pg.Rect(118, 283, 289, 80)
        rating_box = pg.Rect(118, 383, 289, 80)

        start_bg = pg.image.load("images/BG/menu.jpg")
        self.screen.blit(start_bg, (0, 0))

        font = pg.font.Font(self.generalFont, 45)
        self.screen.blit(pg.font.Font(self.generalFont, 120).render('2048', True, config.COLORS['WHITE']), (108, 60))
        self.screen.blit(font.render('PLAY', True, config.COLORS['WHITE']), (210, 270))
        self.screen.blit(font.render('RATING', True, config.COLORS['WHITE']), (186, 370))

        pg.display.update()

        pressed_button = False
        while not pressed_button:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    elif event.key == pg.K_RETURN:
                        self.put_name()
                        pressed_button = True
                    elif event.key == 114:
                        self.draw_top_gamers()
                        pressed_button = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if play_box.collidepoint(event.pos):
                        self.put_name()
                        pressed_button = True
                    elif rating_box.collidepoint(event.pos):
                        self.draw_top_gamers()
                        pressed_button = True

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
        self.screen.blit(pg.transform.scale(pg.image.load("images/BG/BG.jpg"), (self.width, self.height + 2)), (0, 0))
        self.screen.blit(pg.transform.scale(pg.image.load("images/elements/around_arrow.png"), (43, 43)), (453, 159))
        self.screen.blit(pg.transform.scale(pg.image.load("images/elements/arrow.png"), (58, 58)), (374, 154))
        self.screen.blit(pg.transform.scale(pg.image.load("images/elements/home.png"), (38, 38)), (314, 162))

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
            (447 - correct, 77))

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

    @abstractmethod
    def update(self) -> None:
        """Updating the game status"""
        pass

    @abstractmethod
    def handle_events(self) -> None:
        """Handles actions entered by the player"""
        pass

    @abstractmethod
    def run(self) -> None:
        """Launches the game"""
        pass
