import pygame as pg


def get_index_from_number(num: int) -> tuple[int, int]:
    """Returns a tuple with indices based on the board cell number"""
    num -= 1
    return num // 4, num % 4


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
