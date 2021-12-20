import pygame as pg


class Point:
    __slots__ = ('_x', '_y')

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def get_side(self) -> str:
        if self._x > 0 and self._y >= 0:  # 1st quarter
            if self._x == self._y or self._x < self._y:
                return 'UP'
            return 'RIGHT'
        if self._x <= 0 < self._y:  # 2nd quarter
            if abs(self._x) == self._y or abs(self._x) > self._y:
                return 'LEFT'
            return 'UP'
        if self._x < 0 and self._y <= 0:  # 3rd quarter
            if self._x == self._y or abs(self._x) < abs(self._y):
                return 'DOWN'
            return 'LEFT'
        if self._y < 0 <= self._x:  # 4th quarter
            if self._x == abs(self._y) or self._x > abs(self._y):
                return 'RIGHT'
            return 'DOWN'


def quick_copy(mas: list) -> list:
    return [[value for value in row] for row in mas]


def get_index_from_number(num: int) -> tuple[int, int]:
    """Returns a tuple with indices based on the board cell number"""
    num -= 1
    return num // 4, num % 4


def get_side(dot_one: tuple, dot_two: tuple) -> tuple[str, int]:
    """Returns the main side of the swipe. top, bottom, left, right + distance"""
    x = dot_two[0] - dot_one[0]
    y = dot_one[1] - dot_two[1]
    distance = (x ** 2 + y ** 2) ** 0.5
    point = Point(x, y)
    print(f'x ={x} y={y}', distance)
    result_side = point.get_side()
    return result_side, distance


def get_number_from_index(x: int, y: int) -> int:
    """Returns the number at the indices of the board cell"""
    return x * 4 + y + 1


def get_size_font(score_size: int, score_top_size: int) -> tuple[int, int]:
    """Returns a tuple with two values to substitute the text of the values on the screen."""
    SIZE_SCORE, SCORE_TOP_SIZE = len(str(abs(score_size))), len(str(abs(score_top_size)))
    if SIZE_SCORE == 6 and SCORE_TOP_SIZE == 6:
        return 20, 20
    elif SIZE_SCORE == 6 or SCORE_TOP_SIZE == 6:
        if SIZE_SCORE == 6 and SCORE_TOP_SIZE != 6:
            return 22, 25
        return 25, 20
    else:
        return 25, 25


def get_const_4_cell(value: int, gen_font: str) -> tuple[int, object]:
    """Returns the size for the font and the font itself as a tuple"""
    size = 50
    font = pg.font.Font(gen_font, size)
    if value > 512:
        size = 40
        font = pg.font.Font(gen_font, size)
        if value > 8192:
            size = 30
            font = pg.font.Font(gen_font, size)
            if value > 65536:
                size = 25
                font = pg.font.Font(gen_font, size)
                if value >= 1048576:
                    return 'WTF?!', font
                return value, font
            return value, font
        return value, font
    return value, font
