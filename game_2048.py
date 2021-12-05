from interface import Interface


class Game2048(Interface):
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
