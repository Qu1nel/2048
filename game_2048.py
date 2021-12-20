import json
import os
import sys

import pygame as pg

import config
from board import GameBoard
from interface import Interface


class Game2048(Interface):

    def __init__(self):
        super().__init__()
        self.board = GameBoard()
        self.copy_board = None

    def put_name(self) -> None:
        def _render(self) -> None:
            name_bg = pg.image.load("images\\BG\\input_username.jpg")
            menu = pg.image.load("images\\elements\\home.png")
            self.screen.blit(pg.font.Font(
                self.generalFont, 120).render('2048', True, config.COLORS['WHITE']), (108, 60))
            self.screen.blit(name_bg, (0, 0))
            self.screen.blit(pg.transform.scale(menu, [50, 50]), (236, 494))
            self.screen.blit(pg.font.Font(self.generalFont, 45).render('OK', True, config.COLORS['WHITE']), (229, 371))

        active_colour = '#013df2'
        inactive_colour = '#33346b'
        ok_box = pg.Rect(118, 383, 289, 80)
        input_box = pg.Rect(118, 283, 289, 80)
        menu_box = pg.Rect(225, 483, 75, 75)

        _render(self)
        font_input = pg.font.Font(self.generalFont, 48)
        pg.draw.rect(self.screen, color := inactive_colour, input_box, 1, border_radius=15)
        pg.display.update()

        name = ''
        active = False
        input_name = False
        while not input_name:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    active = True if input_box.collidepoint(event.pos) else False
                    if ok_box.collidepoint(event.pos):
                        if len(name) >= 3:
                            self.username = name
                            input_name = True
                    elif menu_box.collidepoint(event.pos):
                        self.draw_menu()
                        return None
                    color = active_colour if active else inactive_colour
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if active:
                        if event.key == pg.K_RETURN:
                            if len(name) >= 3:
                                self.username = name
                                input_name = True
                        elif event.key == pg.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            if font_input.render(name, True, config.COLORS['WHITE']).get_width() < 261:
                                name += event.unicode
            _render(self)
            if name == '' and color == inactive_colour:
                self.screen.blit(font_input.render('Username', True, config.COLORS['GRAY']), (155, 267))
            txt = font_input.render(name, True, config.COLORS['WHITE'])
            pg.draw.rect(self.screen, color, input_box, 1, border_radius=15)
            self.screen.blit(txt, (input_box.w - txt.get_width() // 2 - 26, 267))
            pg.display.update()

    def load_game(self):
        path = os.getcwd()
        if 'save.txt' in os.listdir(path):
            with open('save.txt') as file:
                data = json.load(file)
                self.board = GameBoard(data['board'])
                self.score = data['score']
                self.username = data['user']
            full_path = os.path.join(path, 'save.txt')
            os.remove(full_path)
        else:
            self.__init__()

    def save_game(self):
        """Saves the game"""
        data = dict(user=self.username, score=self.score, board=self.board.get_mas)
        with open('save.txt', 'w') as outfile:
            json.dump(data, outfile)

    def update(self):
        self.board.insert_in_mas()
        self.draw_main()
        pg.display.update()

    def is_victory(self) -> bool:
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.save_game()
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    save_game()
                    pygame.quit()
                    sys.exit()
                elif event.key == pg.K_LEFT or event.key == pg.K_a:  # Left
                    self.board.move_left(self)
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:  # Right
                    self.board.move_right(self)
                elif event.key == pg.K_UP or event.key == pg.K_w:  # Up
                    self.board.move_up(self)
                elif event.key == pg.K_DOWN or event.key == pg.K_s:  # Down
                    self.board.move_down(self)
                self.update()
                if self.is_victory():
                    self.draw_victory()

    def run(self):
        try:
            while True:
                self.load_game()
                if self.username is None:
                    self.draw_menu()
                self.draw_main()
                while self.board.are_there_zeros() and self.board.can_move():
                    self.handle_events()

                    pg.display.update()
                    self.clock.tick(self.framerate)
                self.draw_game_over()
        except Exception as exc:
            self.save_game()
            raise exc


def main() -> None:
    Game2048().run()


if __name__ == '__main__':
    main()
