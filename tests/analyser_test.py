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
        attempt = Attempt(1000, 30, 2, 1000, 30, 2)
        statistic = Analyser.analyse(frame, Strategy.counter_cyclical, broker, Statistic(), attempt)
        inventory = {'AAA': {'price': 0, 'number': 0}, 'CCC': {'price': 0, 'number': 0}}
        for test_data in statistic.test_data:
            action = test_data['action']
            number = test_data['number']
            ticker = test_data['ticker']
            price = test_data['price']
            total_price = price * number
            if action is Action.BUY and cash >= total_price:
                cash = cash - total_price - 3.9
                inventory[ticker]['number'] = inventory[ticker]['number'] + number
                inventory[ticker]['price'] = price
            elif action is Action.SELL and inventory[ticker]['number'] >= number:
                cash = cash + total_price - 3.9
                inventory[ticker]['number'] = inventory[ticker]['number'] - number
                inventory[ticker]['price'] = price
            else:
                continue
        self.assertEqual(broker.inventory['AAA'].number, inventory['AAA']['number'])
        self.assertEqual(broker.inventory['AAA'].price, inventory['AAA']['price'])
        self.assertEqual(broker.inventory['CCC'].number, inventory['CCC']['number'])
        self.assertEqual(broker.inventory['CCC'].price, inventory['CCC']['price'])
        self.assertEqual(broker.cash, cash)
        self.assertGreater(broker.funds(), initial_cash)
