import unittest  # noqa

from sliding_blocks import a_star, State


class TestSlidingBlocks(unittest.TestCase):
    """docstring for TestSlidingBlocks."""
    @staticmethod
    def read_user_input(start, end):
        """"Imitate reading user input."""
        return State(start), State(end)

    def test_with_zero_slide(self):
        """Start and final positions are the same."""
        solution = a_star(*TestSlidingBlocks.read_user_input(
            [1, 2, 3, 4, 5, 6, 7, 8, 0], [1, 2, 3, 4, 5, 6, 7, 8, 0]))
        self.assertEqual(solution.path, 0)

    def test_with_one_slide(self):
        """Final position is reached after one move."""
        solution = a_star(*TestSlidingBlocks.read_user_input(
            [1, 2, 3, 4, 5, 6, 7, 0, 8], [1, 2, 3, 4, 5, 6, 7, 8, 0]))
        self.assertEqual(solution.path, 1)

    def test_with_two_slides(self):
        """Final position is reached after two moves."""
        solution = a_star(*TestSlidingBlocks.read_user_input(
            [1, 2, 3, 4, 5, 6, 0, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8, 0]))
        self.assertEqual(solution.path, 2)


if __name__ == '__main__':
    unittest.main()
