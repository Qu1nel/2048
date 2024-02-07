from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pygame as pg


@dataclass(slots=True)
class Point:  # noqa: D101
    x: int
    y: int

    def get_side(self) -> str:  # noqa: D102
        if self.x > 0 and self.y >= 0:  # 1st quarter
            if self.x == self.y or self.x < self.y:
                return "UP"
            return "RIGHT"
        if self.x <= 0 < self.y:  # 2nd quarter
            if abs(self.x) == self.y or abs(self.x) > self.y:
                return "LEFT"
            return "UP"
        if self.x < 0 and self.y <= 0:  # 3rd quarter
            if self.x == self.y or abs(self.x) < abs(self.y):
                return "DOWN"
            return "LEFT"
        if (self.y < 0 <= self.x) and (self.x == abs(self.y) or self.x > abs(self.y)):  # 4th quarter
            return "RIGHT"
        return "DOWN"


def quick_copy(data: Any) -> list:
    """Return a copy of game board."""
    mas = [] if data is None else data.get_mas
    return [list(row) for row in mas]


def get_index_from_number(num: int) -> tuple[int, int]:
    """Returns a tuple with indices based on the board cell number."""
    num -= 1
    return num // 4, num % 4


def get_side(dot_one: tuple, dot_two: tuple) -> tuple[str, int]:
    """Returns the main side of the swipe. top, bottom, left, right + distance."""
    x = dot_two[0] - dot_one[0]
    y = dot_one[1] - dot_two[1]
    distance = (x**2 + y**2) ** 0.5
    point = Point(x, y)
    print(f"x ={x} y={y}", distance)
    result_side = point.get_side()
    return result_side, distance


def get_number_from_index(x: int, y: int) -> int:
    """Returns the number at the indices of the board cell."""
    return x * 4 + y + 1


def get_size_font(score_size: int, score_top_size: int) -> tuple[int, int]:
    """Returns a tuple with two values to substitute the text of the values on the screen."""
    size_score = len(str(abs(score_size)))
    score_top_size = len(str(abs(score_top_size)))

    if size_score == 6 and score_top_size == 6:  # noqa: PLR2004
        return 20, 20
    if size_score == 6 or score_top_size == 6:  # noqa: PLR2004
        if size_score == 6 and score_top_size != 6:  # noqa: PLR2004
            return 22, 25
        return 25, 20
    return 25, 25


def get_const_4_cell(value: int, gen_font: Path) -> tuple[int, pg.font.FontType]:
    """Returns the size for the font and the font itself as a tuple."""
    size = 50
    font = pg.font.Font(gen_font, size)
    if value > 512:  # noqa: PLR2004
        size = 40
        font = pg.font.Font(gen_font, size)
        if value > 8192:  # noqa: PLR2004
            size = 30
            font = pg.font.Font(gen_font, size)
            if value > 65536:  # noqa: PLR2004
                size = 25
                font = pg.font.Font(gen_font, size)
                return value, font
            return value, font
        return value, font
    return value, font
