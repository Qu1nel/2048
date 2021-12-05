from random import random, shuffle, randint
from typing import Any

from logics_TMP import get_index_from_number


class GameBoard(object):
    def __init__(self):
        self.__mas = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.is_board_move = None

        FIRST_SLOT, SECOND_SLOT = randint(1, 16), randint(1, 16)
        while FIRST_SLOT == SECOND_SLOT:  # In case the random cells are the same
            FIRST_SLOT, SECOND_SLOT = randint(1, 16), randint(1, 16)

        self.insert_2_or_4(*get_index_from_number(FIRST_SLOT))
        self.insert_2_or_4(*get_index_from_number(SECOND_SLOT))

    def __getitem__(self, item: int) -> list:
        return self.__mas[item]

    def __setitem__(self, key: int, value: Any):
        self.__mas[key] = value

    def __iter__(self):
        return iter(self.__mas)

    def are_there_zeros(self) -> bool:
        """Checks if there is a 0 in the board"""
        for row in self:
            if 0 in row:
                return True
        return False

    def get_empty_list(self) -> list:
        """Returns a list with empty cell numbers"""
        return [get_number_from_index(i, y) for i in range(4) for y in range(4) if self[i][y] == 0]

    def insert_in_mas(self) -> None:
        """Inserts randomly 2 or 4 into the game board DURING the game process"""
        if self.is_board_move and self.are_there_zeros():
            self.is_board_move = False
            empty = self.get_empty_list()  # List of empty cells
            shuffle(empty)  # List gets in the way
            random_num = empty.pop()  # Selects a random item
            x, y = get_index_from_number(random_num)
            self.insert_2_or_4(x, y)

    def insert_2_or_4(self, x: int, y: int) -> None:
        """Inserts a random of 2 and 4 into the cell [x, y]"""
        if random() <= 0.90:
            self[x][y] = 2
        else:
            self[x][y] = 4

    def can_move(self) -> bool:
        """Checks if an action can be taken"""
        for i in range(3):
            for y in range(3):
                if self[i][y] == self[i][y + 1] or self[i][y] == self[i + 1][y]:
                    return True
        for i in range(3, 0, -1):
            for y in range(3, 0, -1):
                if self[i][y] == self[i][y - 1] or self[i][y] == self[i - 1][y]:
                    return True
        return False
