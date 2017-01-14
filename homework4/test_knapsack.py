from collections import OrderedDict
from Knapsack import knapsack
import unittest


class TestBranchAndBound(unittest.TestCase):
    def test_with_three_items(self):
        result = knapsack(
            OrderedDict({(3, 2): 0, (1, 5): 0, (2, 3): 0}),
            5, 3)
        self.assertEqual(8, result)

    # def test_with_three_items(self):
    #     result = knapsack(
    #         OrderedDict({(3, 5): 0, (2, 3): 0, (1, 4): 0}),
    #         5, 3)
    #     self.assertEqual(9, result)

    # def test_with_four_items(self):
    #     result = knapsack(
    #         OrderedDict({(9, 45): 0, (3, 45): 0, (5, 10): 0, (5, 30): 0}),
    #         16, 4)
    #     self.assertEqual(90, result)

    # def test_with_five_items(self):
    #     result = knapsack(
    #         OrderedDict({(1, 50): 0, (56, 30): 0, (42, 20): 0, (78, 10): 0, (12, 50): 0}),
    #         150, 5)
    #     self.assertEqual(150, result)

    # def test_with_seven_items(self):
    #     result = knapsack(
    #         OrderedDict({(1, 11): 0, (21, 31): 0, (23, 33): 0, (33, 43): 0, (43, 53): 0, (45, 55): 0, (55, 65): 0}),
    #         110, 7)
    #     self.assertEqual(150, result)


if __name__ == '__main__':
    unittest.main()
