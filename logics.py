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
        """ Выдает основное направление по x и y точки.

        :return: str
        """
        if self._x > 0 and self._y >= 0:  # 1-ая четверть
            if self._x == self._y or self._x < self._y:
                return 'ВВЕРХ'
            return 'ВПРАВО'
        if self._x <= 0 < self._y:  # 2-ая четверть
            if abs(self._x) == self._y or abs(self._x) > self._y:
                return 'ВЛЕВО'
            return 'ВВЕРХ'
        if self._x < 0 and self._y <= 0:  # 3-ая четверть
            if self._x == self._y or abs(self._x) < abs(self._y):
                return 'ВНИЗ'
            return 'ВЛЕВО'
        if self._y < 0 <= self._x:  # 4-ая четверть
            if self._x == abs(self._y) or self._x > abs(self._y):
                return 'ВПРАВО'
            return 'ВНИЗ'


def pretty_print(mas: list) -> None:
    """ Красиво выводит в консоль состояние матрицы

    :param mas: игровая матрица mas
    :return: None
    """
    print('-' * 21)
    for row in mas:
        for j in row:
            print(str(j).ljust(6), end=' ')
        print()
    print('-' * 21)


def insert_2_or_4(mas: list, x: int, y: int) -> list:
    """ Вставляет в указанную ячейку матрицы 2 или 4 возвращая обнавленнцю матрицу

     2 с вероятностью 90%
    4 с вероятностью 10%

    :param mas: игровая матрица mas
    :param x: строка mas
    :param y: столбец mas
    :return: обнавленный mas
    """
    if random() <= 0.90:  # Выбор вероятности для выпадений 2
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas


def get_number_from_index(i: int, j: int) -> int:
    """ Возвращает число по индексам ячейки матрицы.

    :param i: индекс по строке матрицы
    :param j: индекс по столбцу матрицы
    :return: int Число [1-16]
    """
    return i * 4 + j + 1


def get_index_from_number(num: int) -> tuple[int, int]:
    """ Возвращает кортеж с индексоами по номеру ячейки матрицы.

    :param num: число ячейки матрицы
    :return: tuple вида: (int, int)
    """
    num -= 1
    return num // 4, num % 4


def get_empty_list(mas: list) -> list:
    """ Возвращает список с номерами пустых ячеик.

    :param mas: игровая матрица list
    :return: список с номерами пустых клеток
    """
    empty = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                empty.append(get_number_from_index(i, j))
    return empty


def is_zero_in_mas(mas: list) -> bool:
    """ Проверяет, есть ли 0 в матрице.

    :param mas: игровая матрица list
    :return: Булевый тип
    """
    for row in mas:
        if 0 in row:
            return True
    return False


def move_left(mas: list) -> tuple[list, int, bool]:
    """ Возвращает обновленную матрицу со смещенными по правилу игры элементами влево.

    :param mas: игровая матрица list
    :return: обнавленный игровая матрица list
    """
    # сохранить превоначальное значения матрицы
    origin = copy.deepcopy(mas)  # deepcopy копирует многомерный матрица без привязки к оригиналу
    delta = 0  # сумма изменений ячеек, для результата
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
    """ Возвращает обновленную матрицу со смещенными по правилу игры элементами вправо.

    :param mas: игровая матрица list
    :return: обнавленный игровая матрица list
    """
    origin = copy.deepcopy(mas)
    delta = 0  # сумма изменений ячеек, для результата
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
    """ Возвращает обновленную матрицу со смещенными по правилу игры элементами вверх.

    :param mas: игровая матрица list
    :return: обнавленный игровая матрица list
    """
    origin = copy.deepcopy(mas)
    delta = 0  # сумма изменений ячеек, для результата
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
    """ Возвращает обновленную матрицу со смещенными по правилу игры элементами вниз.

    :param mas: игровая матрица list
    :return: обнавленный игровая матрица list
    """
    origin = copy.deepcopy(mas)
    delta = 0  # сумма изменений ячеек, для результата
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
    """ Проверяет, Проверяет можно ли сделать дейсвтие.

    :param mas: игровая матрица list
    :return: Булевый тип
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
    """ Возвращает число, обозначающее сколько цифр в числе.
    Возвращает 0 для чисел до 10.

    :param number: любое число int
    :return: количество цифр в нём int
    """
    number //= 10
    total = 0
    while number:
        number //= 10
        total += 1
    return total


def get_size_font(score_size: int, score_top_size: int) -> tuple[int, int]:
    """ Возвращает кортеж с двумя значениями, для подстановки текста значений на экране

    :param score_size: Значение score, для счетчика score
    :param score_top_size: Значение лучшего игрока, для счетчика лучшего результата
    :return: кортеж с двумя значениями - (int, int)
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
    """ Возвращает число для более точного урегулирования текста на экране

    :param number_size: Размер шрифта
    :param number: Самой значение текста
    :return: Одно число для учета погрешности
    """
    if number_size == 35:
        return is_what_rank_numbers(number) * 7
    return is_what_rank_numbers(number) * 8


def get_colour(value: int) -> str:
    """ По переданному числу возвращает его цвет на клетке

    :param value: Число которое должно быть на игровом поле
    :return: Цвет числа
    """
    if value in (2, 4):
        return '#545E66'  # GRAY
    return '#ebeeff'  # WHITE


def get_const_4_cell(value: int, gen_font: str) -> tuple[int, object]:
    """ Возвращает кортеж с числом и шрифтом в котором доллжно нарисоваться это число

    :param value: Значение из клетки
    :param gen_font: Шрифт каким будет нарисован значение на экране
    :return: Кортеж с числом которое нужно вывести, и шрифтом
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
    """ get_side(dot_one: tuple, dot_two: tuple) -> tuple[str, int].
    Возвращает основную стороку свайпа, т.е. верх, низ, лево, право + расстояние

    :param dot_one: Первая точка - (x, y)
    :param dot_two: Вторая точка - (x, y)
    :return: Кортеж со стороной и расстоянием между точками - ("сторона", расстояние)
    """
    x = dot_two[0] - dot_one[0]
    y = dot_one[1] - dot_two[1]
    distance = (x ** 2 + y ** 2) ** 0.5
    point = Point(x, y)
    print(f'x ={x} y={y}', distance)
    result_side = point.get_side()
    return result_side, distance


def get_font(number: int, font: str) -> pygame.font.Font:
    """ Задает размер дефолтного шрифта

    :param number: размер шрифта int
    :param font: путь до шрифта
    :return: сам шрифт
    """
    return pygame.font.Font(font, number)
