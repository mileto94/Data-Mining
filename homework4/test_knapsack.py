from collections import OrderedDict
from Knapsack import knapsack
import unittest


class TestBranchAndBound(unittest.TestCase):
    def test_with_three_items(self):
        result = knapsack(
            OrderedDict({(2, 3): 0, (5, 1): 0, (3, 2): 0}),
            5, 3)
        self.assertEqual(8, result)

    def test_with_three_items_again(self):
        result = knapsack(
            OrderedDict({(5, 3): 0, (3, 2): 0, (4, 1): 0}),
            5, 3)
        self.assertEqual(9, result)

    def test_with_four_items(self):
        result = knapsack(
            OrderedDict({(45, 9): 0, (45, 3): 0, (10, 5): 0, (30, 5): 0}),
            16, 4)
        self.assertEqual(90, result)

    def test_with_five_items(self):
        result = knapsack(
            OrderedDict({(50, 1): 0, (30, 56): 0, (20, 42): 0, (10, 78): 0, (50, 12): 0}),
            150, 5)
        self.assertEqual(150, result)

    def test_with_seven_items(self):
        result = knapsack(
            OrderedDict({(11, 1): 0, (31, 21): 0, (33, 23): 0, (43, 33): 0, (53, 43): 0, (55, 45): 0, (65, 55): 0}),
            110, 7)
        self.assertEqual(150, result)


if __name__ == '__main__':
    unittest.main()