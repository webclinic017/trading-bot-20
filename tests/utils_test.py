import math
import unittest

from src.utils import Utils


class MyTestCase(unittest.TestCase):
    def test_valid(self):
        valid = Utils.valid(1, 2, 3)
        self.assertEqual(valid, True)
        valid = Utils.valid(3, 2, 3)
        self.assertEqual(valid, False)
        valid = Utils.valid(1, 2, 1)
        self.assertEqual(valid, False)

    def test_negation(self):
        negation = Utils.negation()
        self.assertGreaterEqual(negation, -1)
        self.assertLessEqual(negation, 1)

    def test_inverse(self):
        inverse = Utils.inverse()
        self.assertGreaterEqual(inverse, 0)
        self.assertLessEqual(inverse, math.inf)

    def test_group(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        group = Utils.group(3, iterable)
        self.assertTupleEqual(group, ((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        group = Utils.group(2, iterable)
        self.assertTupleEqual(group, ((1, 2), (3, 4), (5, 6), (7, 8)))

    def test_number(self):
        number = Utils.number(6.3, 2.4)
        self.assertEqual(number, 2)
        number = Utils.number(9.2, 2.9)
        self.assertEqual(number, 3)
        number = Utils.number(0, 0)
        self.assertEqual(number, 0)


if __name__ == '__main__':
    unittest.main()
