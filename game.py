from __future__ import annotations

from abc import abstractmethod

import pygame as pg


class Game(object):
    """A class with all the main attributes of the game (game window)"""
    caption: str
    width: int
    height: int
    icon: str  # path to image
    framerate: int | float

    def __init__(self, caption, width, height, icon, framerate=60):
        pg.init()
        pg.display.set_caption(caption)
        pg.display.set_icon(pg.image.load(icon))
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.framerate = framerate
        self.width = width
        self.height = height
        self.victory = False
        self.username = None
        self.score, self.old_score = 0, 0

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
