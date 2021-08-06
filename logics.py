from random import random
import pygame
import copy

__all__ = [
    'Point',
    'can_move',
    'get_colour',
    'get_const_4_cell',
    'get_empty_list',
    'get_font',
    'get_index_from_number',
    'get_number_from_index',
    'get_side',
    'get_size_font',
    'get_var_for_size',
    'insert_2_or_4',
    'is_what_rank_numbers',
    'is_zero_in_mas',
    'move_down',
    'move_left',
    'move_right',
    'move_up',
    'pretty_print'
]


class Point:
    __slots__ = ['_x', '_y']

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def get_side(self) -> str:
        """ Gives the main x and y direction of a point.

        :return: str
        """
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


def pretty_print(mas: list) -> None:
    """ Nicely displays the state of the matrix to the console

    :param mas: game matrix
    :return: None
    """
    print('-' * 21)
    for row in mas:
        for j in row:
            print(str(j).ljust(6), end=' ')
        print()
    print('-' * 21)


def insert_2_or_4(mas: list, x: int, y: int) -> list:
    """ Inserts a 2 or 4 matrix into the specified cell, returning an updated matrix

     2 with a 90% probability
    4 with a probability of 10%

    :param mas: game matrix
    :param x: row mas
    :param y: column mas
    :return: updated matrix
    """
    if random() <= 0.90:
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas


def get_number_from_index(i: int, j: int) -> int:
    """ Returns the number at the indices of the matrix cell.

    :param i: matrix row index
    :param j: matrix column index
    :return: number [1-16]
    """
    return i * 4 + j + 1


def get_index_from_number(num: int) -> tuple[int, int]:
    """ Returns a tuple with indices based on the matrix cell number.

    :param num: number of matrix cells
    :return: tuple of the form (int, int)
    """
    num -= 1
    return num // 4, num % 4


def get_empty_list(mas: list) -> list:
    """ Returns a list with empty cell numbers.

    :param mas: game matrix
    :return: list with numbers of empty cells
    """
    empty = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                empty.append(get_number_from_index(i, j))
    return empty


def is_zero_in_mas(mas: list) -> bool:
    """ Checks if there is a 0 in the matrix.

    :param mas: game matrix
    :return: bool
    """
    for row in mas:
        if 0 in row:
            return True
    return False


def move_left(mas: list) -> tuple[list, int, bool]:
    """ Returns the updated matrix with game-shifted elements to the left.

    :param mas: game matrix
    :return: updated play matrix
    """
    # keep the original values of the matrix
    origin = copy.deepcopy(mas)
    delta = 0  # sum of cell changes, for the result
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)

    for i in range(4):
        for k in range(3):
            if mas[i][k] != 0 and mas[i][k] == mas[i][k + 1]:
                mas[i][k] *= 2
                delta += mas[i][k]
                mas[i].pop(k + 1)
                mas[i].append(0)
    return mas, delta, not origin == mas


def move_right(mas: list) -> tuple[list, int, bool]:
    """ Returns the updated matrix with game-shifted elements right.

    :param mas: game matrix
    :return: updated play matrix
    """
    origin = copy.deepcopy(mas)
    delta = 0  # sum of cell changes, for the result
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)

    for i in range(4):
        for k in range(3, 0, -1):
            if mas[i][k] != 0 and mas[i][k] == mas[i][k - 1]:
                mas[i][k] *= 2
                delta += mas[i][k]
                mas[i].pop(k - 1)
                mas[i].insert(0, 0)
    return mas, delta, not origin == mas


def move_up(mas: list) -> tuple[list, int, bool]:
    """ Returns the updated matrix with game-shifted elements up.

    :param mas: game matrix
    :return: updated play matrix
    """
    origin = copy.deepcopy(mas)
    delta = 0  # sum of cell changes, for the result
    for j in range(4):
        column = []
        for i in range(4):
            if mas[i][j] != 0:
                column.append(mas[i][j])
        while len(column) != 4:
            column.append(0)
        for i in range(3):
            if column[i] != 0 and column[i] == column[i + 1]:
                column[i] *= 2
                delta += column[i]
                column.pop(i + 1)
                column.append(0)
        for i in range(4):
            mas[i][j] = column[i]
    return mas, delta, not origin == mas


def move_down(mas: list) -> tuple[list, int, bool]:
    """ Returns the updated matrix with game-shifted elements downward.

    :param mas: game matrix
    :return: updated play matrix
    """
    origin = copy.deepcopy(mas)
    delta = 0  # sum of cell changes, for the result
    for j in range(4):
        column = []
        for i in range(4):
            if mas[i][j] != 0:
                column.append(mas[i][j])
        while len(column) != 4:
            column.insert(0, 0)
        for i in range(3, 0, -1):
            if column[i] != 0 and column[i] == column[i - 1]:
                column[i] *= 2
                delta += column[i]
                column.pop(i - 1)
                column.insert(0, 0)
        for i in range(4):
            mas[i][j] = column[i]
    return mas, delta, not origin == mas


def can_move(mas: list) -> bool:
    """ Checks if an action can be taken.

    :param mas: game matrix
    :return: bool
    """
    for i in range(3):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] or mas[i][j] == mas[i + 1][j]:
                return True
    for i in range(3, 0, -1):
        for j in range(3, 0, -1):
            if mas[i][j] == mas[i][j - 1] or mas[i][j] == mas[i - 1][j]:
                return True
    return False


def is_what_rank_numbers(number: int) -> int:
    """ Returns a number indicating how many digits are in a number.
    Returns 0 for numbers up to 10.

    :param number: any int
    :return: the number of digits
    """
    number //= 10
    total = 0
    while number:
        number //= 10
        total += 1
    return total


def get_size_font(score_size: int, score_top_size: int) -> tuple[int, int]:
    """ Returns a tuple with two values to substitute the text of the values on the screen

    :param score_size: value of the score
    :param score_top_size: value of the hight score
    :return: a tuple with two values (int, int)
    """
    SIZE_SCORE = is_what_rank_numbers(score_size)
    SCORE_TOP_SIZE = is_what_rank_numbers(score_top_size)
    if SIZE_SCORE == 6 and SCORE_TOP_SIZE == 6:
        return 20, 20
    elif SIZE_SCORE == 6 or SCORE_TOP_SIZE == 6:
        if SIZE_SCORE == 6 and SCORE_TOP_SIZE != 6:
            return 22, 25
        return 25, 20
    else:
        return 25, 25


def get_var_for_size(number_size: int, number: int) -> int:
    """ Returns a number for more precise adjustment of the text on the screen

    :param number_size: Size of the font
    :param number: value of the text
    :return: int
    """
    if number_size == 35:
        return is_what_rank_numbers(number) * 7
    return is_what_rank_numbers(number) * 8


def get_colour(value: int) -> str:
    """ Returns its color on the cell as given

    :param value: The number that must be on the playing field
    :return: color of the cell
    """
    if value in (2, 4):
        return '#545E66'  # GRAY
    return '#ebeeff'  # WHITE


def get_const_4_cell(value: int, gen_font: str) -> tuple[int, object]:
    """ Returns a tuple with a number and a font in which this number should be drawn

    :param value: Value out of the cage
    :param gen_font: Font of the text
    :return: tuple
    """
    size = 50
    font = pygame.font.Font(gen_font, size)
    if value > 512:
        size = 40
        font = pygame.font.Font(gen_font, size)
        if value > 8192:
            size = 30
            font = pygame.font.Font(gen_font, size)
            if value > 65536:
                size = 25
                font = pygame.font.Font(gen_font, size)
                if value >= 1048576:
                    return 'WTF?!', font
                return value, font
            return value, font
        return value, font
    return value, font


def get_side(dot_one: tuple, dot_two: tuple) -> tuple[str, int]:
    """ Returns the main side of the swipe. top, bottom, left, right + distance

    :param dot_one: First point - (x, y)
    :param dot_two: Second point - (x, y)
    :return: tuple
    """
    x = dot_two[0] - dot_one[0]
    y = dot_one[1] - dot_two[1]
    distance = (x ** 2 + y ** 2) ** 0.5
    point = Point(x, y)
    print(f'x ={x} y={y}', distance)
    result_side = point.get_side()
    return result_side, distance


def get_font(number: int, font: str) -> pygame.font.Font:
    """ Sets the size of the default font

    :param number: size of the font int
    :param font: path to font
    :return: font
    """
    return pygame.font.Font(font, number)
