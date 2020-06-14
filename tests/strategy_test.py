import unittest

import pandas as pd

from src.attempt import Attempt
from src.strategy import Strategy


class StrategyTest(unittest.TestCase):
    def test_buy(self):
        data = {'IBM': [10, 1]}
        frame = pd.DataFrame(data)
        attempt = Attempt(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                          amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = Strategy.counter_cyclical(frame, 1, 0, attempt)
        self.assertEqual(action, 'buy')
        self.assertEqual(number, 1000)

    def test_sell(self):
        data = {'IBM': [1, 10]}
        frame = pd.DataFrame(data)
        attempt = Attempt(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                          amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = Strategy.counter_cyclical(frame, 1, 0, attempt)
        self.assertEqual(action, 'sell')
        self.assertEqual(number, 100)

    def test_none(self):
        data = {'IBM': [1, 1]}
        frame = pd.DataFrame(data)
        attempt = Attempt(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                          amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = Strategy.counter_cyclical(frame, 1, 0, attempt)
        self.assertEqual(action, 'none')
        self.assertEqual(number, 0)


if __name__ == '__main__':
    unittest.main()
