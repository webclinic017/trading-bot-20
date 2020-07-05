import unittest

from src.action import Action
from src.analyser import Analyser
from src.attempt import Attempt
from src.broker import Broker
from src.statistic import Statistic
from src.strategy import Strategy
from tests.utils import Utils


class AnalyserTestCase(unittest.TestCase):

    def test_analyser(self):
        frame = Utils.create_frame()
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
            if action is Action.BUY and cash >= total_price:
                cash = cash - total_price - 3.9
                number = number + 10
                value = number * price
            elif action is Action.SELL and number >= 2:
                cash = cash + price * 2 - 3.9
                number = number - 2
                value = number * price
            else:
                continue
            self.assertEqual(cash, statistic.test_data[i]['cash'])
            self.assertEqual(value, statistic.test_data[i]['inventory.value'])
            self.assertEqual(number, statistic.test_data[i]['inventory.number'])
        self.assertGreater(broker.funds(), initial_cash)
