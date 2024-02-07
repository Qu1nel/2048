"""Game 2048 written in Python, pygame module. First pet-project. cringe..."""

import pygame as pg  # type: ignore

from src.config import CAPTION, ICON_PATH, resource_path
from src.main import App

__author__ = "Qu1nel"
__version__ = "1.0"

pg.init()
pg.display.set_caption(CAPTION)

try:
    icon = pg.image.load(resource_path(ICON_PATH))
    pg.display.set_icon(icon)
except FileNotFoundError:
    pass

GameApp2048 = App()


def start() -> None:
    """Enter point in game 2048."""
    GameApp2048.run()
