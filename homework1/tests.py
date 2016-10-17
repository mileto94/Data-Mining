import unittest
from homework import dfs, create_state, call_dfs



class TestCreateStates(unittest.TestCase):
    def test_empty_start_and_end(self):
        n = 0
        count, start, end = create_state(n)
        self.assertEqual(start, [])
        self.assertEqual(end, [])
        self.assertEqual(count, n)

    def test_start_and_end_with_one_frog(self):
        n = 1
        count, start, end = create_state(n * 2)
        self.assertEqual(start, [1, 0, 2])
        self.assertEqual(end, [2, 0, 1])
        self.assertEqual(count, n)

    def test_start_and_end_with_five_frogs(self):
        n = 5
        count, start, end = create_state(n * 2)
        self.assertEqual(start, [1, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2])
        self.assertEqual(end, [2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1])
        self.assertEqual(count, n)


class TestDFSFrogs(unittest.TestCase):
    def test_empty_equal_start_and_end(self):
        n = 0
        count, start, end = create_state(0)
        self.assertTrue(dfs(start, end=end))
        self.assertEqual(count, n)

    def test_with_one_frog(self):
        n = 1
        count, start, end = create_state(n * 2)
        self.assertEqual(count, n)
        self.assertTrue(dfs(start, end=end, zero_index=count))

    def test_with_five_frogs(self):
        n = 5
        count, start, end = create_state(n * 2)
        self.assertEqual(count, n)
        self.assertTrue(dfs(start, end=end, zero_index=count))

    def test_with_ten_frogs(self):
        n = 10
        count, start, end = create_state(n * 2)
        self.assertEqual(count, n)
        self.assertTrue(dfs(start, end=end, zero_index=count))

    def test_with_twenty_frogs(self):
        n = 20
        count, start, end = create_state(n * 2)
        self.assertEqual(count, n)
        self.assertTrue(dfs(start, end=end, zero_index=count))


class TestCallingFunction(unittest.TestCase):
    def test_with_one_frog(self):
        self.assertTrue(call_dfs(2))

    def test_with_two_frogs(self):
        self.assertTrue(call_dfs(4))

    def test_with_five_frogs(self):
        self.assertTrue(call_dfs(6))


if __name__ == '__main__':
    unittest.main()
