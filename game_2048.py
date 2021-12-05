from board import GameBoard
from interface import Interface


class Game2048(Interface):

    def __init__(self):
        super().__init__()
        self.board = GameBoard()
        self.copy_board = None
        self.score, self.old_score = None, None
        self.username = None

    def run(self):
        pass
        # self.load_game()
        # while self.board.are_there_zeros() and self.board.can_move():
        #     self.handle_events()
        #
        #     pg.display.update()
        #     self.clock.tick(self.framerate)


def main() -> None:
    Game2048().run()


if __name__ == '__main__':
    main()
