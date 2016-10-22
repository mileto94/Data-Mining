import unittest  # noqa

from game import sliding_blocks


class TestSlidingBlocks(unittest.TestCase):
    """docstring for TestSlidingBlocks."""

    def test_with_zero_sliding(self):
        self.assertEqual(sliding_blocks(0, []), 0)


if __name__ == '__main__':
    unittest.main()
