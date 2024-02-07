import json
import os
import sys
from pathlib import Path

import pygame as pg

from src import config, database
from src.board import GameBoard
from src.config import BG_PATH, CAPTION, ELEMENTS_PATH, MIN_NAME_LENGTH
from src.interface import Interface
from src.logics import get_side, quick_copy


class App(Interface):
    """The main game class that implements all the necessary logic.

    Attributes:
        board: Board of game.
        copy_board: Copy of board.
        move_mouse: A flag.
        position: A mouse coord click.

    """

    board: GameBoard
    copy_board: list
    move_mouse: bool
    position: tuple[int, int]

    def __init__(self) -> None:
        """Init base attribute."""
        super().__init__()
        self.board = GameBoard()
        self.move_mouse = False

    def put_name(self) -> None:
        """Drawing screen "put name"."""

        def _render(game: Interface) -> None:
            name_bg = pg.image.load(BG_PATH / Path("input_username.jpg"))
            menu = pg.image.load(ELEMENTS_PATH / Path("home.png"))
            game.screen.blit(
                pg.font.Font(game.generalFont, 120).render(CAPTION, antialias=True, color=config.COLORS["WHITE"]),
                (108, 60),
            )
            game.screen.blit(name_bg, (0, 0))
            game.screen.blit(pg.transform.scale(menu, [50, 50]), (236, 494))
            game.screen.blit(
                pg.font.Font(game.generalFont, 45).render("OK", antialias=True, color=config.COLORS["WHITE"]),
                (229, 371),
            )

        active_colour = "#013df2"
        inactive_colour = "#33346b"
        ok_box = pg.Rect(118, 383, 289, 80)
        input_box = pg.Rect(118, 283, 289, 80)
        menu_box = pg.Rect(225, 483, 75, 75)

        _render(self)
        font_input = pg.font.Font(self.generalFont, 48)
        pg.draw.rect(self.screen, color := inactive_colour, input_box, 1, border_radius=15)
        pg.display.update()

        name = ""
        active = False
        input_name = False
        while not input_name:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    active = bool(input_box.collidepoint(event.pos))
                    if ok_box.collidepoint(event.pos):
                        if len(name) >= MIN_NAME_LENGTH:
                            self.username = name
                            input_name = True
                    elif menu_box.collidepoint(event.pos):
                        self.draw_menu()
                        return
                    color = active_colour if active else inactive_colour
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if active:
                        if event.key == pg.K_RETURN:
                            if len(name) >= MIN_NAME_LENGTH:
                                self.username = name
                                input_name = True
                        elif event.key == pg.K_BACKSPACE:
                            name = name[:-1]
                        elif (
                            font_input.render(name, antialias=True, color=config.COLORS["WHITE"]).get_width()
                            < 261  # noqa: PLR2004
                        ):
                            name += event.unicode
            _render(self)
            if name == "" and color == inactive_colour:
                self.screen.blit(font_input.render("Username", antialias=True, color=config.COLORS["GRAY"]), (155, 267))
            txt = font_input.render(name, antialias=True, color=config.COLORS["WHITE"])
            pg.draw.rect(self.screen, color, input_box, 1, border_radius=15)
            self.screen.blit(txt, (input_box.w - txt.get_width() // 2 - 26, 267))
            pg.display.update()

    def load_game(self) -> None:
        """Loads a last game from save."""
        path = Path.cwd()
        if "save.txt" in os.listdir(path):
            with open("save.txt") as file:
                data = json.load(file)
                self.board = GameBoard(data["board"])
                self.score = data["score"]
                self.username = data["user"]
            full_path = path / Path("save.txt")
            Path(full_path).unlink()
        else:
            super().__init__()
            self.board = GameBoard()
            self.move_mouse = False

    def save_game(self) -> None:
        """Saves the game."""
        data = {"user": self.username, "score": self.score, "board": self.board.get_mas}
        with open("save.txt", "w") as outfile:
            json.dump(data, outfile)

    def update(self) -> None:
        """Update board, drawing screen and update screen."""
        self.board.insert_in_mas()
        self.draw_main()
        pg.display.update()

    def is_victory(self) -> bool:
        """Check victory on board."""
        return any(2048 in row for row in self.board)  # noqa: PLR2004

    def around_arrow(self) -> None:
        """Drawing screen during click on "around arrow" in play process."""
        cancel_box = pg.Rect(145, 415, 150, 70)
        repeat_box = pg.Rect(305, 415, 150, 70)

        blur = pg.Surface((self.width, self.height), pg.SRCALPHA)
        blur.fill((0, 0, 0, 140))
        self.screen.blit(blur, (0, 0))

        self.screen.blit(
            pg.font.Font(self.generalFont, 53).render("Reset game?", antialias=True, color=config.COLORS["WHITE"]),
            (60, 200),
        )
        font_h3 = pg.font.Font(self.generalFont, 32)
        self.screen.blit(
            font_h3.render("Are you sure you wish to", antialias=True, color=config.COLORS["WHITE"]),
            (60, 300),
        )
        self.screen.blit(font_h3.render("reset the game?", antialias=True, color=config.COLORS["WHITE"]), (60, 340))

        pg.draw.rect(self.screen, (110, 110, 110), cancel_box, border_radius=12)
        self.screen.blit(font_h3.render("Cancel", antialias=True, color=config.COLORS["WHITE"]), (174, 413))

        pg.draw.rect(self.screen, (110, 110, 110), repeat_box, border_radius=12)
        self.screen.blit(font_h3.render("Reset", antialias=True, color=config.COLORS["WHITE"]), (341, 413))
        pg.display.update()

        make_decision = False
        while not make_decision:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.save_game()
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key in (pg.K_BACKSPACE, pg.K_ESCAPE):  # cancel
                        self.update()
                        make_decision = True
                    elif event.key == pg.K_RETURN:  # reset
                        super().__init__()
                        self.board = GameBoard()
                        self.update()
                        make_decision = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if cancel_box.collidepoint(event.pos):  # cancel
                        self.update()
                        make_decision = True
                    elif repeat_box.collidepoint(event.pos):  # reset
                        super().__init__()
                        self.board = GameBoard()
                        self.update()
                        make_decision = True

    def back_arrow(self) -> None:
        """Drawing screen during click on "back arrow" in play process."""
        if self.copy_board is not None and self.copy_board != self.board.get_mas:
            self.board.get_mas = [list(row) for row in self.copy_board]
            self.score = self.old_score
            self.draw_main()
            pg.display.update()

    def handle_events(self) -> bool:
        """Handle all events from user."""
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
                if back_arrow_box.collidepoint(event.pos):  # Back arrow
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
                        if source_swipe[1] > 30:  # noqa: PLR2004
                            command_side = {
                                "UP": self.board.move_up,
                                "DOWN": self.board.move_down,
                                "LEFT": self.board.move_left,
                                "RIGHT": self.board.move_right,
                            }
                            self.copy_board = quick_copy(self.board)
                            command_side[source_swipe[0]](self)
                            self.update()
                            if self.is_victory():
                                self.draw_victory()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.save_game()
                    pg.quit()
                    sys.exit()
                elif event.key in (pg.K_LEFT, pg.K_a):  # Left
                    self.copy_board = quick_copy(self.board)
                    self.board.move_left(self)
                elif event.key in (pg.K_RIGHT, pg.K_d):  # Right
                    self.copy_board = quick_copy(self.board)
                    self.board.move_right(self)
                elif event.key in (pg.K_UP, pg.K_w):  # Up
                    self.copy_board = quick_copy(self.board)
                    self.board.move_up(self)
                elif event.key in (pg.K_DOWN, pg.K_s):  # Down
                    self.copy_board = quick_copy(self.board)
                    self.board.move_down(self)
                self.update()
                if self.is_victory():
                    self.draw_victory()
        return False

    def run(self) -> None:
        """Launch the game."""
        try:
            while True:
                self.load_game()
                if self.username is None:
                    self.draw_menu()
                self.draw_main()
                while self.board.are_there_zeros() and self.board.can_move():
                    pg.display.update()
                    if self.handle_events() is True:
                        break
                    pg.display.update()
                    self.clock.tick(self.framerate)
                else:
                    self.draw_game_over()
        except Exception:  # noqa: BLE001
            self.save_game()
