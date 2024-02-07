"""Game 2048 written in Python, pygame module. First pet-project. cringe..."""

import sys
from pathlib import Path

import pygame as pg  # type: ignore

from src.config import CAPTION, ICON_PATH
from src.main import App

__author__ = "Qu1nel"
__version__ = "1.0"


def resource_path(relative_path: Path) -> Path:
    """Function for working paths inside an exe for python."""
    base_path = Path(getattr(sys, "_MEIPASS", ".")).absolute()
    return base_path.joinpath(relative_path)


pg.init()

try:
    icon = pg.image.load(resource_path(ICON_PATH))
    pg.display.set_icon(icon)
except FileNotFoundError:
    pass

pg.display.set_caption(CAPTION)

GameApp2048 = App()


def start() -> None:
    """Enter point in game 2048."""
    GameApp2048.run()
