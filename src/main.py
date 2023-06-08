import json
import os
import sys

import pygame as pg

import src.config as config
import src.database as database
from src.board import GameBoard
from src.config import APP_PATH
from src.interface import Interface
from src.logics import get_side, quick_copy


class Game2048(Interface):

    def __init__(self):
        super().__init__()
        self.board = GameBoard()
        self.copy_board = None
        self.move_mouse = False
        self.position = None

    def put_name(self) -> None:
        def _render(game) -> None:
            name_bg = pg.image.load(f"{APP_PATH}/images/BG/input_username.jpg")
            menu = pg.image.load(f"{APP_PATH}/images/elements/home.png")
            game.screen.blit(pg.font.Font(
                game.generalFont, 120).render('2048', True, config.COLORS['WHITE']), (108, 60))
            game.screen.blit(name_bg, (0, 0))
            game.screen.blit(pg.transform.scale(menu, [50, 50]), (236, 494))
            game.screen.blit(pg.font.Font(game.generalFont, 45).render('OK', True, config.COLORS['WHITE']), (229, 371))

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

    def around_arrow(self):
        cancel_box = pg.Rect(145, 415, 150, 70)
        repeat_box = pg.Rect(305, 415, 150, 70)

        blur = pg.Surface((self.width, self.height), pg.SRCALPHA)
        blur.fill((0, 0, 0, 140))
        self.screen.blit(blur, (0, 0))

        self.screen.blit(pg.font.Font(
            self.generalFont, 53).render('Reset game?', True, config.COLORS['WHITE']), (60, 200))
        font_H3 = pg.font.Font(self.generalFont, 32)
        self.screen.blit(font_H3.render('Are you sure you wish to', True, config.COLORS['WHITE']), (60, 300))
        self.screen.blit(font_H3.render('reset the game?', True, config.COLORS['WHITE']), (60, 340))

        pg.draw.rect(self.screen, (110, 110, 110), cancel_box, border_radius=12)
        self.screen.blit(font_H3.render('Cancel', True, config.COLORS['WHITE']), (174, 413))

        pg.draw.rect(self.screen, (110, 110, 110), repeat_box, border_radius=12)
        self.screen.blit(font_H3.render('Reset', True, config.COLORS['WHITE']), (341, 413))
        pg.display.update()

        make_decision = False
        while not make_decision:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    save_game()
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE or event.key == pg.K_ESCAPE:  # cancel
                        self.update()
                        make_decision = True
                    elif event.key == pg.K_RETURN:  # reset
                        super().__init__()
                        self.board = GameBoard()
                        self.copy_board = None
                        self.update()
                        make_decision = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if cancel_box.collidepoint(event.pos):  # cancel
                        self.update()
                        make_decision = True
                    elif repeat_box.collidepoint(event.pos):  # reset
                        super().__init__()
                        self.board = GameBoard()
                        self.copy_board = None
                        self.update()
                        make_decision = True

    def back_arrow(self) -> None:
        if self.copy_board is not None and self.copy_board != self.board.get_mas:
            self.board.get_mas = quick_copy(self.copy_board)
            self.score = self.old_score
            self.draw_main()
            pg.display.update()

    def handle_events(self):
        repeat_box = pg.Rect(447, 153, 58, 58)
        menu_box = pg.Rect(305, 153, 58, 58)
        back_arrow_box = pg.Rect(376, 153, 58, 58)
        play_ground = pg.Rect(15, 225, 488, 488)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.save_game()
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:  # Clicked on the mouse button
                if menu_box.collidepoint(event.pos):  # Menu
                    database.insert_result(self.username, self.score)
                    self.username = None
                    return True
                elif back_arrow_box.collidepoint(event.pos):  # Back arrow
                    self.back_arrow()
                elif repeat_box.collidepoint(event.pos):  # Encapsulated arrow
                    self.around_arrow()
                elif play_ground.collidepoint(event.pos):  # Swipe mouse part 1
                    self.move_mouse = True
                    self.position = event.pos
            elif event.type == pg.MOUSEBUTTONUP:  # Released the mouse button
                if self.move_mouse:  # Swipe mouse part 2
                    self.move_mouse = False
                    if self.position != event.pos:
                        source_swipe = get_side(self.position, event.pos)
                        if source_swipe[1] > 30:
                            command_side = {'UP': self.board.move_up, 'DOWN': self.board.move_down,
                                            'LEFT': self.board.move_left, 'RIGHT': self.board.move_right}
                            self.copy_board = quick_copy(self.board.get_mas)
                            command_side[source_swipe[0]](self)
                            self.update()
                            if self.is_victory():
                                self.draw_victory()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    save_game()
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_LEFT or event.key == pg.K_a:  # Left
                    self.copy_board = quick_copy(self.board.get_mas)
                    self.board.move_left(self)
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:  # Right
                    self.copy_board = quick_copy(self.board.get_mas)
                    self.board.move_right(self)
                elif event.key == pg.K_UP or event.key == pg.K_w:  # Up
                    self.copy_board = quick_copy(self.board.get_mas)
                    self.board.move_up(self)
                elif event.key == pg.K_DOWN or event.key == pg.K_s:  # Down
                    self.copy_board = quick_copy(self.board.get_mas)
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
                    pg.display.update()
                    if self.handle_events():
                        break
                    pg.display.update()
                    self.clock.tick(self.framerate)
                else:
                    self.draw_game_over()
        except Exception as exc:
            self.save_game()
            raise exc


def main() -> None:
    Game2048().run()
