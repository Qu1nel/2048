from random import randint, random, shuffle
from typing import Any, Union

from src.logics import get_index_from_number, get_number_from_index, quick_copy


class GameBoard(object):
    def __init__(self, mas: list = None):
        if mas is not None:
            self.__mas = mas
        else:
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

    def __setitem__(self, key: int, value: Any) -> Union[list, int]:
        self.__mas[key] = value

    def __iter__(self):
        return iter(self.__mas)

    def move_left(self, game):
        """Moves the board to the left"""
        origin = quick_copy(self.get_mas)
        game.delta = 0
        for row in self:
            while 0 in row:
                row.remove(0)
            while len(row) != 4:
                row.append(0)

        for x in range(4):
            for y in range(3):
                if self[x][y] != 0 and self[x][y] == self[x][y + 1]:
                    self[x][y] *= 2
                    game.old_score = game.score
                    game.score += self[x][y]
                    game.delta += self[x][y]
                    self[x].pop(y + 1)
                    self[x].append(0)
        self.is_board_move = not origin == self.get_mas

    def move_right(self, game):
        """Moves the board to the right"""
        origin = quick_copy(self.get_mas)
        game.delta = 0
        for row in self:
            while 0 in row:
                row.remove(0)
            while len(row) != 4:
                row.insert(0, 0)

        for x in range(4):
            for y in range(3, 0, -1):
                if self[x][y] != 0 and self[x][y] == self[x][y - 1]:
                    self[x][y] *= 2
                    game.old_score = game.score
                    game.score += self[x][y]
                    game.delta += self[x][y]
                    self[x].pop(y - 1)
                    self[x].insert(0, 0)
        self.is_board_move = not origin == self.get_mas

    def move_up(self, game):
        """Moves the board to the up"""
        origin = quick_copy(self.get_mas)
        game.delta = 0
        for y in range(4):
            column = []
            for x in range(4):
                if self[x][y] != 0:
                    column.append(self[x][y])
            while len(column) != 4:
                column.append(0)
            for x in range(3):
                if column[x] != 0 and column[x] == column[x + 1]:
                    column[x] *= 2
                    game.old_score = game.score
                    game.score += column[x]
                    game.delta += column[x]
                    column.pop(x + 1)
                    column.append(0)
            for x in range(4):
                self[x][y] = column[x]
        self.is_board_move = not origin == self.get_mas

    def move_down(self, game):
        """Moves the board to the down"""
        origin = quick_copy(self.get_mas)
        game.delta = 0
        for y in range(4):
            column = []
            for x in range(4):
                if self[x][y] != 0:
                    column.append(self[x][y])
            while len(column) != 4:
                column.insert(0, 0)
            for x in range(3, 0, -1):
                if column[x] != 0 and column[x] == column[x - 1]:
                    column[x] *= 2
                    game.old_score = game.score
                    game.score += column[x]
                    game.delta += column[x]
                    column.pop(x - 1)
                    column.insert(0, 0)
            for x in range(4):
                self[x][y] = column[x]
        self.is_board_move = not origin == self.get_mas

    @property
    def get_mas(self):
        return self.__mas

    @get_mas.setter
    def get_mas(self, value):
        self.__mas = value

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
