from decimal import Decimal

from pandas import date_range, DataFrame

from tests.base_test_case import BaseTestCase
from trading_bot.bo.strategy_bo import StrategyBO
from trading_bot.dto.attempt_dto import AttemptDTO
from trading_bot.enums.action_enum import ActionEnum


class StrategyBOTestCase(BaseTestCase):

    def setUp(self):
        self.attempt = AttemptDTO(amount_buy=Decimal('1000'), distance_buy=Decimal('1'), delta_buy=Decimal('1.5'),
                                  amount_sell=Decimal('1000'), distance_sell=Decimal('1'), delta_sell=Decimal('1.5'))

    def test_counter_cyclical_buy(self):
        intraday_list = self.get_intraday_frame(data=[10, 1])
        action, number = StrategyBO.counter_cyclical(intraday_list, self.attempt)
        self.assertEqual(action, ActionEnum.BUY)
        self.assertEqual(number, 1000)

    def test_counter_cyclical_sell(self):
        intraday_list = self.get_intraday_frame(data=[1, 10])
        action, number = StrategyBO.counter_cyclical(intraday_list, self.attempt)
        self.assertEqual(action, ActionEnum.SELL)
        self.assertEqual(number, 100)

    def test_counter_cyclical_none(self):
        intraday_list = self.get_intraday_frame(data=[1, 1])
        action, number = StrategyBO.counter_cyclical(intraday_list, self.attempt)
        self.assertEqual(action, ActionEnum.NONE)
        self.assertEqual(number, 0)

    def test_volume_trading_buy(self):
        intraday_list = self.get_intraday_frame(data=[10, 1])
        action, number = StrategyBO.volume_trading(intraday_list, self.attempt)
        self.assertEqual(action, ActionEnum.BUY)
        self.assertEqual(number, 1000)

    def test_volume_trading_sell(self):
        intraday_list = self.get_intraday_frame(data=[1, 10])
        action, number = StrategyBO.volume_trading(intraday_list, self.attempt)
        self.assertEqual(action, ActionEnum.SELL)
        self.assertEqual(number, 100)

    def test_volume_trading_none(self):
        intraday_list = self.get_intraday_frame(data=[1, 1])
        action, number = StrategyBO.volume_trading(intraday_list, self.attempt)
        self.assertEqual(action, ActionEnum.NONE)
        self.assertEqual(number, 0)

    @staticmethod
    def get_intraday_frame(start='1/1/2000', data=None):
        dates = date_range(start, periods=len(data))
        columns = ['open', 'high', 'low', 'close', 'volume']
        frame = DataFrame(columns=columns)
        for i in range(len(data)):
            frame.loc[i] = [float(data[i]) for _ in range(5)]
        frame['date'] = dates
        frame.sort_index(inplace=True, ascending=True)
        return frame
