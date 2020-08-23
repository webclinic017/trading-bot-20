import unittest
from decimal import Decimal

from src.bo.analyser_bo import AnalyserBO
from src.bo.broker_bo import BrokerBO
from src.bo.statistic_bo import StatisticBO
from src.bo.strategy_bo import StrategyBO
from src.constants import ZERO
from src.dto.attempt_dto import AttemptDTO
from src.enums.action_enum import ActionEnum
from tests.utils.utils import Utils


class AnalyserBOTestCase(unittest.TestCase):

    def test_analyser(self):
        frame = Utils.create_table_frame()
        broker = BrokerBO(cash=Decimal('10000'), fee=Decimal('3.9'))
        initial_cash = broker.cash
        cash = broker.cash
        attempt = AttemptDTO(Decimal('1000'), Decimal('30'), Decimal('2'), Decimal('1000'), Decimal('30'), Decimal('2'))
        statistic = AnalyserBO.analyse(frame, StrategyBO.counter_cyclical, broker, StatisticBO(), attempt)
        inventory = {'AAA': {'price': ZERO, 'number': ZERO},
                     'CCC': {'price': ZERO, 'number': ZERO}}
        for test_data in statistic.test_data:
            action = test_data['action']
            number = test_data['number']
            ticker = test_data['ticker']
            price = test_data['price']
            total_price = price * number
            if action is ActionEnum.BUY and cash >= total_price:
                cash = cash - total_price - Decimal('3.9')
                inventory[ticker]['number'] = inventory[ticker]['number'] + number
                inventory[ticker]['price'] = price
            elif action is ActionEnum.SELL and inventory[ticker]['number'] >= number:
                cash = cash + total_price - Decimal('3.9')
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
