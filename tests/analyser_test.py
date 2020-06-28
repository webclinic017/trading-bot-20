import math
import unittest

import numpy as np
import pandas as pd

from src.analyser import Analyser
from src.attempt import Attempt
from src.broker import Broker
from src.statistic import Statistic
from src.strategy import Strategy


class AnalyserTestCase(unittest.TestCase):

    def test_analyser(self):
        dates = pd.date_range('1/1/2000', periods=150)
        prices_aaa = np.full((150, 1), float(500))
        prices_aaa[30:60] = float(100)
        prices_aaa[90:120] = float(100)
        prices_bbb = np.full((150, 1), float(500))
        prices_bbb[0:30] = math.nan
        tickers = ['AAA', 'BBB']
        prices = np.hstack((prices_aaa, prices_bbb))
        frame = pd.DataFrame(prices, index=dates, columns=tickers)
        frame.sort_index(inplace=True, ascending=False)
        broker = Broker()
        initial_cash = broker.cash
        cash = broker.cash
        number = 0
        attempt = Attempt(1000, 30, 2, 1000, 30, 2)
        statistic = Analyser.analyse(frame, Strategy.counter_cyclical, broker, Statistic(), attempt)

        for i in range(len(statistic.test_data)):
            action = statistic.test_data[i]['action']
            price = statistic.test_data[i]['inventory.price']
            total_price = price * 10
            if action == 'buy' and cash >= total_price:
                cash = cash - total_price - 3.9
                number = number + 10
                value = number * price
            elif action == 'sell' and number >= 2:
                cash = cash + price * 2 - 3.9
                number = number - 2
                value = number * price
            else:
                continue
            self.assertEqual(cash, statistic.test_data[i]['cash'])
            self.assertEqual(value, statistic.test_data[i]['inventory.value'])
            self.assertEqual(number, statistic.test_data[i]['inventory.number'])
        self.assertGreater(broker.funds(), initial_cash)
