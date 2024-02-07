from abc import abstractmethod

import pygame as pg

from src.config import Size


class Game:
    """A class with all the main attributes of the game (game window).

    Attributes:
        screen: Surface for drawing.
        clock: Tactics for fps.
        width: Window widths.
        height: Window heights.

    Methods:
        update(self, /) -> None: Drawing Cardioid object on display by "self.app".

        handle_events(self, /) -> None: Handles actions entered by the player.

        run(self, /) -> None: Launches the game.

    """

    screen: pg.SurfaceType
    clock: pg.time.Clock
    framerate: int
    width: int
    height: int
    victory: bool
    username: str | None
    score: int
    old_score: int

    def __init__(self, size: Size, framerate: int = 60) -> None:
        """Init base attribute."""
        self.screen = pg.display.set_mode((size.width, size.height))
        self.clock = pg.time.Clock()
        self.framerate = framerate
        self.width = size.width
        self.height = size.height
        self.victory = False
        self.username = None
        self.score, self.old_score = 0, 0

    @abstractmethod
    def update(self) -> None:
        """Updating the game status."""

    @abstractmethod
    def handle_events(self) -> bool:
        """Handles actions entered by the player."""

    @abstractmethod
    def run(self) -> None:
        """Launches the game."""
