import unittest
from typing import Dict, List

import pandas as pd
from pandas import DataFrame

from src.bo.strategy_bo import StrategyBO
from src.dto.attempt_dto import AttemptDTO
from src.enums.action_enum import ActionEnum


class StrategyBOTestCase(unittest.TestCase):
    def test_buy(self):
        frame = StrategyBOTestCase.create_frame({'IBM': [10, 1]})
        attempt = AttemptDTO(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                             amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = StrategyBO.counter_cyclical(frame, 'IBM', frame.index.max(), attempt)
        self.assertEqual(action, ActionEnum.BUY)
        self.assertEqual(number, 1000)

    def test_sell(self):
        frame = StrategyBOTestCase.create_frame({'IBM': [1, 10]})
        attempt = AttemptDTO(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                             amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = StrategyBO.counter_cyclical(frame, 'IBM', frame.index.max(), attempt)
        self.assertEqual(action, ActionEnum.SELL)
        self.assertEqual(number, 100)

    def test_none(self):
        frame = StrategyBOTestCase.create_frame({'IBM': [1, 1]})
        attempt = AttemptDTO(amount_buy=1000, distance_buy=1, delta_buy=1.5,
                             amount_sell=1000, distance_sell=1, delta_sell=1.5)
        action, number = StrategyBO.counter_cyclical(frame, 'IBM', frame.index.max(), attempt)
        self.assertEqual(action, ActionEnum.NONE)
        self.assertEqual(number, 0)

    @staticmethod
    def create_frame(data: Dict[str, List[int]]) -> DataFrame:
        dates = pd.date_range('1/1/2000', periods=2, freq='1d')
        frame = pd.DataFrame(data, index=dates)
        frame.sort_index(inplace=True, ascending=True)
        return frame


if __name__ == '__main__':
    unittest.main()
