import unittest  # noqa

from game import sliding_blocks


class TestSlidingBlocks(unittest.TestCase):
    """docstring for TestSlidingBlocks."""

    def test_with_zero_sliding(self):
        """Start and final positions are the same."""
        self.assertEqual(
            sliding_blocks(3, [[1, 2], [3, 0]], [[1, 2], [3, 0]]),
            0)

    def test_with_one_sliding(self):
        """Final position is reached after one move."""
        self.assertEqual(
            sliding_blocks(3, [[1, 2], [0, 3]], [[1, 2], [3, 0]]),
            1)


if __name__ == '__main__':
    unittest.main()
