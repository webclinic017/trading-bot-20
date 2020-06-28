import unittest
from typing import Dict, List

import pandas as pd
from pandas import DataFrame

from src.action import Action
from src.attempt import Attempt
from src.strategy import Strategy


class StrategyTestCase(unittest.TestCase):
    def test_buy(self):
        frame = StrategyTestCase.create_frame({'IBM': [10, 1]})
        attempt = Attempt(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                          amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = Strategy.counter_cyclical(frame, 'IBM', frame.index.max(), attempt)
        self.assertEqual(action, Action.BUY)
        self.assertEqual(number, 1000)

    def test_sell(self):
        frame = StrategyTestCase.create_frame({'IBM': [1, 10]})
        attempt = Attempt(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                          amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = Strategy.counter_cyclical(frame, 'IBM', frame.index.max(), attempt)
        self.assertEqual(action, Action.SELL)
        self.assertEqual(number, 100)

    def test_none(self):
        frame = StrategyTestCase.create_frame({'IBM': [1, 1]})
        attempt = Attempt(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                          amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = Strategy.counter_cyclical(frame, 'IBM', frame.index.max(), attempt)
        self.assertEqual(action, Action.NONE)
        self.assertEqual(number, 0)

    @staticmethod
    def create_frame(data: Dict[str, List[int]]) -> DataFrame:
        dates = pd.date_range('1/1/2000', periods=2, freq='1d')
        frame = pd.DataFrame(data, index=dates)
        frame.sort_index(inplace=True, ascending=False)
        return frame


if __name__ == '__main__':
    unittest.main()
