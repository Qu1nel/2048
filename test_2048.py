import unittest
from logics import *


class MyTestCase(unittest.TestCase):

    def test_1(self):
        self.assertEqual(get_number_from_index(1, 2), 7)

    def test_2(self):
        self.assertEqual(get_number_from_index(3, 3), 16)

    def test_3(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        mas = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(get_empty_list(mas), a)

    def test_4(self):
        a = [5, 6, 7, 8, 9, 10, 12, 13, 15, 16]
        mas = [
            [1, 2, 1, 2],
            [0, 0, 0, 0],
            [0, 0, 5, 0],
            [0, 6, 0, 0]
        ]
        self.assertEqual(get_empty_list(mas), a)

    def test_5(self):
        a = []
        mas = [
            [1, 2, 1, 2],
            [1, 2, 1, 2],
            [1, 2, 1, 2],
            [1, 2, 1, 2]
        ]
        self.assertEqual(get_empty_list(mas), a)

    def test_6(self):
        self.assertEqual(get_index_from_number(7), (1, 2))

    def test_7(self):
        self.assertEqual(get_index_from_number(16), (3, 3))

    def test_8(self):
        self.assertEqual(get_index_from_number(1), (0, 0))

    def test_9(self):
        mas = [
            [1, 2, 1, 2],
            [1, 2, 1, 2],
            [1, 2, 1, 2],
            [1, 2, 1, 2]
        ]
        self.assertEqual(is_zero_in_mas(mas), False)

    def test_10(self):
        mas = [
            [1, 2, 1, 2],
            [1, 2, 0, 2],
            [1, 2, 1, 2],
            [1, 2, 1, 2]
        ]
        self.assertEqual(is_zero_in_mas(mas), True)

    def test_11(self):
        mas = [
            [1, 2, 1, 2],
            [1, 0, 1, 2],
            [1, 2, 0, 2],
            [0, 2, 1, 2]
        ]
        self.assertEqual(is_zero_in_mas(mas), True)

    def test_12(self):
        mas = [
            [2, 2, 0, 0],
            [0, 4, 0, 4],
            [0, 0, 128, 0],
            [64, 0, 64, 0]
        ]
        rez = [
            [0, 0, 0, 4],
            [0, 0, 0, 8],
            [0, 0, 0, 128],
            [0, 0, 0, 128]
        ]
        self.assertEqual(move_right(mas), (rez, 140, True))

    def test_13(self):
        mas = [
            [2, 2, 8, 2],
            [0, 4, 16, 4],
            [32, 32, 2, 0],
            [2, 8, 8, 4]
        ]
        rez = [
            [4, 8, 2, 0],
            [4, 16, 4, 0],
            [64, 2, 0, 0],
            [2, 16, 4, 0]
        ]
        self.assertEqual(move_left(mas), (rez, 84, True))

    def test_14(self):
        mas = [
            [2, 4, 0, 2],
            [2, 128, 2, 0],
            [4, 128, 2, 4],
            [4, 4, 0, 16]
        ]
        rez = [
            [4, 4, 4, 2],
            [8, 256, 0, 4],
            [0, 4, 0, 16],
            [0, 0, 0, 0]
        ]
        self.assertEqual(move_up(mas), (rez, 272, True))

    def test_15(self):
        mas = [
            [2, 4, 16, 2],
            [8, 64, 2, 2],
            [8, 0, 2, 32],
            [4, 4, 16, 0]
        ]
        rez = [
            [0, 0, 0, 0],
            [2, 4, 16, 0],
            [16, 64, 4, 4],
            [4, 4, 16, 32]
        ]
        self.assertEqual(move_down(mas), (rez, 24, True))

    def test_16(self):
        mas = [
            [2, 4, 0, 2],
            [2, 0, 2, 0],
            [4, 0, 2, 4],
            [4, 4, 0, 0]
        ]
        self.assertEqual(can_move(mas), True)

    def test_17(self):
        mas = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ]
        self.assertEqual(can_move(mas), False)

    def test_18(self):
        mas = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 8],
            [13, 14, 15, 16]
        ]
        self.assertEqual(can_move(mas), True)

    def test_19(self):
        mas = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [2, 2, 15, 16]
        ]
        self.assertEqual(can_move(mas), True)

    def test_20(self):
        mas = [
            [2, 4, 128, 2],
            [8, 16, 64, 32],
            [4, 512, 16, 4],
            [2, 32, 4, 2]
        ]
        self.assertEqual(can_move(mas), False)

    def test_21(self):
        mas = [
            [2, 4, 32, 2],
            [16, 64, 128, 16],
            [2, 32, 16, 4],
            [4, 16, 2, 2]
        ]
        self.assertEqual(can_move(mas), True)

    def test_22(self):
        num = 5
        self.assertEqual(is_what_rank_numbers(num), 0)

    def test_23(self):
        num = 0
        self.assertEqual(is_what_rank_numbers(num), 0)

    def test_24(self):
        num = 9
        self.assertEqual(is_what_rank_numbers(num), 0)

    def test_25(self):
        num = 11
        self.assertEqual(is_what_rank_numbers(num), 1)

    def test_26(self):
        num = 19
        self.assertEqual(is_what_rank_numbers(num), 1)

    def test_27(self):
        num = 100
        self.assertEqual(is_what_rank_numbers(num), 2)

    def test_28(self):
        num = 99
        self.assertEqual(is_what_rank_numbers(num), 1)

    def test_29(self):
        num = 123
        self.assertEqual(is_what_rank_numbers(num), 2)

    def test_30(self):
        num = 912345678
        self.assertEqual(is_what_rank_numbers(num), 8)

    def test_I_1(self):
        self.assertEqual(Point(78, 45).get_side(), 'RIGHT')

    def test_I_2(self):
        self.assertEqual(Point(46, 45).get_side(), 'RIGHT')

    def test_I_3(self):
        self.assertEqual(Point(45, 45).get_side(), 'UP')

    def test_I_4(self):
        self.assertEqual(Point(45, 46).get_side(), 'UP')

    def test_I_5(self):
        self.assertEqual(Point(2, 56).get_side(), 'UP')

    def test_I_6(self):
        self.assertEqual(Point(2, 0).get_side(), 'RIGHT')

    def test_II_1(self):
        self.assertEqual(Point(-10, 90).get_side(), 'UP')

    def test_II_2(self):
        self.assertEqual(Point(-44, 45).get_side(), 'UP')

    def test_II_3(self):
        self.assertEqual(Point(-45, 45).get_side(), 'LEFT')

    def test_II_4(self):
        self.assertEqual(Point(-46, 45).get_side(), 'LEFT')

    def test_II_5(self):
        self.assertEqual(Point(-90, 10).get_side(), 'LEFT')

    def test_II_6(self):
        self.assertEqual(Point(0, 3).get_side(), 'UP')

    def test_III_1(self):
        self.assertEqual(Point(-90, -10).get_side(), 'LEFT')

    def test_III_2(self):
        self.assertEqual(Point(-46, -45).get_side(), 'LEFT')

    def test_III_3(self):
        self.assertEqual(Point(-45, -45).get_side(), 'DOWN')

    def test_III_4(self):
        self.assertEqual(Point(-45, -46).get_side(), 'DOWN')

    def test_III_5(self):
        self.assertEqual(Point(-10, -90).get_side(), 'DOWN')

    def test_III_6(self):
        self.assertEqual(Point(-10, 0).get_side(), 'LEFT')

    def test_IV_1(self):
        self.assertEqual(Point(10, -90).get_side(), 'DOWN')

    def test_IV_2(self):
        self.assertEqual(Point(44, -45).get_side(), 'DOWN')

    def test_IV_3(self):
        self.assertEqual(Point(45, -45).get_side(), 'RIGHT')

    def test_IV_4(self):
        self.assertEqual(Point(46, -45).get_side(), 'RIGHT')

    def test_IV_5(self):
        self.assertEqual(Point(90, -10).get_side(), 'RIGHT')

    def test_IV_6(self):
        self.assertEqual(Point(0, -10).get_side(), 'DOWN')


if __name__ == '__main__':
    unittest.main()
