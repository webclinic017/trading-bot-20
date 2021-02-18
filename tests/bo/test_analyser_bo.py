from decimal import Decimal

from tests.base_test_case import BaseTestCase
from trading_bot.bo.analyser_bo import AnalyserBO
from trading_bot.bo.broker_bo import BrokerBO
from trading_bot.bo.statistic_bo import StatisticBO
from trading_bot.common.constants import ZERO
from trading_bot.dto.attempt_dto import AttemptDTO
from trading_bot.enums.action_enum import ActionEnum
from trading_bot.enums.strategy_enum import StrategyEnum


class AnalyserBOTestCase(BaseTestCase):

    def test_analyser(self):
        intraday_dict = self.create_default_dict()
        broker = BrokerBO(cash=Decimal('10000'), fee=Decimal('3.9'))
        initial_cash = broker.cash
        cash = broker.cash
        attempt = AttemptDTO(Decimal('1000'), Decimal('30'), Decimal('2'), Decimal('1000'), Decimal('30'), Decimal('2'))
        statistic = AnalyserBO.analyse(intraday_dict, StrategyEnum.COUNTER_CYCLICAL, broker, StatisticBO(), attempt)
        inventory = {'AAA': {'price': ZERO, 'number': ZERO},
                     'CCC': {'price': ZERO, 'number': ZERO}}
        for test_data in statistic.test_data:
            action = test_data['action']
            number = test_data['number']
            symbol = test_data['symbol']
            price = test_data['price']
            total_price = price * number
            if action is ActionEnum.BUY and cash >= total_price:
                cash = cash - total_price - Decimal('3.9')
                inventory[symbol]['number'] = inventory[symbol]['number'] + number
                inventory[symbol]['price'] = price
            elif action is ActionEnum.SELL and inventory[symbol]['number'] >= number:
                cash = cash + total_price - Decimal('3.9')
                inventory[symbol]['number'] = inventory[symbol]['number'] - number
                inventory[symbol]['price'] = price
            else:
                continue
        self.assertEqual(broker.inventory['AAA'].number, inventory['AAA']['number'])
        self.assertEqual(broker.inventory['AAA'].price, inventory['AAA']['price'])
        self.assertEqual(broker.inventory['CCC'].number, inventory['CCC']['number'])
        self.assertEqual(broker.inventory['CCC'].price, inventory['CCC']['price'])
        self.assertEqual(broker.inventory['AAA'].number, Decimal('260'))
        self.assertEqual(broker.inventory['AAA'].price, Decimal('500'))
        self.assertEqual(broker.inventory['CCC'].number, Decimal('540'))
        self.assertEqual(broker.inventory['CCC'].price, Decimal('100'))
        self.assertEqual(broker.cash, cash)
        self.assertGreater(broker.funds(), initial_cash)
