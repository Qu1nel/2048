import json
import os
import sys

import pygame as pg

from board import GameBoard
from interface import Interface


class Game2048(Interface):

    def __init__(self):
        super().__init__()
        self.board = GameBoard()
        self.copy_board = None
        self.username = None

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

    def run(self):
        self.load_game()
        self.draw_main()
        while self.board.are_there_zeros() and self.board.can_move():
            self.handle_events()

            pg.display.update()
            self.clock.tick(self.framerate)


def main() -> None:
    Game2048().run()


if __name__ == '__main__':
    main()
