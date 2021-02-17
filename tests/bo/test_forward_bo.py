from datetime import datetime, timedelta
from decimal import Decimal
from json import dumps
from os import remove
from os.path import join, exists
from unittest.mock import patch

import pytz
from pandas import date_range

from tests.base_test_case import BaseTestCase
from trading_bot import db
from trading_bot.bo.broker_bo import BrokerBO
from trading_bot.bo.configuration_bo import ConfigurationBO
from trading_bot.bo.forward_bo import ForwardBO
from trading_bot.bo.inventory_bo import InventoryBO
from trading_bot.common.constants import ZERO, EMPTY
from trading_bot.common.predictor_adapter import PredictorAdapter
from trading_bot.dao.evaluation_dao import EvaluationDAO
from trading_bot.dao.forward_dao import ForwardDAO
from trading_bot.dto.account_dto import AccountDTO
from trading_bot.dto.attempt_dto import AttemptDTO
from trading_bot.entity.intraday_entity import IntradayEntity
from trading_bot.enums.action_enum import ActionEnum
from trading_bot.enums.configuration_enum import ConfigurationEnum
from trading_bot.enums.strategy_enum import StrategyEnum


class ForwardBOTestCase(BaseTestCase):
    PATH_CHECKPOINT_FILE = join('..', '..', 'model', 'test_checkpoint.h5')
    PATH_MODEL_FILE = join('..', '..', 'model', 'test.h5')
    PATH_MODEL_DIR = join('..', '..', 'model')
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))
    STATISTIC_JSON = [{
        'strategy': 'StrategyEnum.COUNTER_CYCLICAL'}, {
        'action': 'ActionEnum.SELL',
        'date': '2000-05-29 04:00:00+00:00',
        'price': '500.0000000000',
        'symbol': 'AAA'}, {
        'action': 'ActionEnum.BUY',
        'date': '2000-05-29 04:00:00+00:00',
        'price': '100.0000000000',
        'symbol': 'CCC'}]

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()
        ConfigurationBO.init()

    @classmethod
    def tearDownClass(cls):
        if exists(cls.PATH_MODEL_FILE):
            remove(cls.PATH_MODEL_FILE)

    # noinspection DuplicatedCode
    @patch('trading_bot.bo.forward_bo.choice')
    @patch('trading_bot.utils.utils.Utils.send_mail')
    @patch('trading_bot.utils.utils.Utils.is_today')
    @patch('trading_bot.utils.utils.Utils.is_working_day_ny')
    @patch('trading_bot.utils.utils.Utils.now')
    def test_start_counter_cyclical(self, now, is_working_day_ny, is_today, send_mail, choice):
        is_today.return_value = False
        is_working_day_ny.return_value = True
        now.return_value = self.OLD_DATE
        choice.return_value = StrategyEnum.COUNTER_CYCLICAL
        ForwardDAO.create_buy('AAA', Decimal('100'), Decimal('10'), Decimal('8996.1'), StrategyEnum.COUNTER_CYCLICAL)
        ForwardDAO.create_buy('BBB', Decimal('100'), Decimal('10'), Decimal('7992.200000000001'),
                              StrategyEnum.COUNTER_CYCLICAL)
        now.return_value = self.YOUNG_DATE
        EvaluationDAO.create(Decimal('40000'), EMPTY, AttemptDTO(), StrategyEnum.COUNTER_CYCLICAL)
        self.persist_default_intraday()
        ForwardBO.start(lambda: ['AAA', 'BBB', 'CCC'])
        send_mail.assert_called_with(dumps(self.STATISTIC_JSON, indent=4, sort_keys=True, default=str))
        self.assertEqual(send_mail.call_count, 1)
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 4)
        self.assert_attributes(rows[0], action=ActionEnum.BUY, cash=Decimal('8996.1'), timestamp=self.OLD_DATE,
                               number=Decimal('10'), price=Decimal('100'), symbol='AAA',
                               strategy=StrategyEnum.COUNTER_CYCLICAL)
        self.assert_attributes(rows[1], action=ActionEnum.BUY, cash=Decimal('7992.2'), timestamp=self.OLD_DATE,
                               number=Decimal('10'), price=Decimal('100'), symbol='BBB',
                               strategy=StrategyEnum.COUNTER_CYCLICAL)
        self.assert_attributes(rows[2], action=ActionEnum.SELL, cash=Decimal('8988.3'), timestamp=self.YOUNG_DATE,
                               number=Decimal('2'), price=Decimal('500'), symbol='AAA',
                               strategy=StrategyEnum.COUNTER_CYCLICAL)
        self.assert_attributes(rows[3], action=ActionEnum.BUY, cash=Decimal('7984.4'), timestamp=self.YOUNG_DATE,
                               number=Decimal('10'), price=Decimal('100'), symbol='CCC',
                               strategy=StrategyEnum.COUNTER_CYCLICAL)

    # noinspection DuplicatedCode
    @patch('trading_bot.bo.forward_bo.choice')
    @patch('trading_bot.utils.utils.Utils.send_mail')
    @patch('trading_bot.utils.utils.Utils.is_today')
    @patch('trading_bot.utils.utils.Utils.is_working_day_ny')
    @patch('trading_bot.utils.utils.Utils.now')
    @patch('trading_bot.bo.portfolio_bo.PortfolioBO.forward_portfolio')
    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_CHECKPOINT_FILE', new=PATH_CHECKPOINT_FILE)
    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_MODEL_FILE', new=PATH_MODEL_FILE)
    @patch('predictor.utils.predictor_utils.PredictorUtils.PATH_MODEL_DIR', new=PATH_MODEL_DIR)
    def test_start_predictor(self, forward_portfolio, now, is_working_day_ny, is_today, send_mail, choice):
        choice.return_value = StrategyEnum.PREDICTOR
        is_today.return_value = False
        is_working_day_ny.return_value = True
        now.return_value = self.OLD_DATE
        forward_portfolio.return_value = ['AAA']
        ForwardDAO.create_buy('AAA', Decimal('100'), Decimal('10'), Decimal('8996.1'), StrategyEnum.PREDICTOR)
        ForwardDAO.create_buy('BBB', Decimal('100'), Decimal('10'), Decimal('7992.200000000001'),
                              StrategyEnum.PREDICTOR)
        now.return_value = self.YOUNG_DATE
        EvaluationDAO.create(Decimal('40000'), EMPTY, AttemptDTO(), StrategyEnum.PREDICTOR)
        self.persist_large_intraday()
        PredictorAdapter.fit(sufficient_data=0, past=self.PAST, future=self.FUTURE)
        IntradayEntity.query.delete()
        self.persist_large_intraday(number=125)
        buy = self.spy_decorator(BrokerBO.buy)
        sell = self.spy_decorator(BrokerBO.sell)
        predict = self.spy_decorator(PredictorAdapter.predict, past=self.PAST, future=self.FUTURE)
        with patch.object(BrokerBO, 'buy', buy), patch.object(BrokerBO, 'sell', sell), \
                patch.object(PredictorAdapter, 'predict', predict):
            ForwardBO.start(lambda: ['AAA'])
        self.assertEqual(buy.mock.call_count, 2)
        self.assertEqual(sell.mock.call_count, 1)
        self.assertEqual(send_mail.call_count, 1)
        ForwardBO.start(lambda: ['AAA'])
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 3)
        self.assert_attributes(rows[0], action=ActionEnum.BUY, cash=Decimal('8996.1'), timestamp=self.OLD_DATE,
                               number=Decimal('10'), price=Decimal('100'), symbol='AAA',
                               strategy=StrategyEnum.PREDICTOR)
        self.assert_attributes(rows[1], action=ActionEnum.BUY, cash=Decimal('7992.2'), timestamp=self.OLD_DATE,
                               number=Decimal('10'), price=Decimal('100'), symbol='BBB',
                               strategy=StrategyEnum.PREDICTOR)
        self.assert_attributes(rows[2], action=ActionEnum.SELL, cash=Decimal('8988.3'), timestamp=self.YOUNG_DATE,
                               number=Decimal('2'), price=Decimal('500'), symbol='AAA',
                               strategy=StrategyEnum.PREDICTOR)

    @patch('trading_bot.utils.utils.Utils.now')
    def test_init(self, now):
        prices = (Decimal('20'), Decimal('30'), Decimal('40'), Decimal('50'), Decimal('60'), Decimal('70'))
        numbers = (Decimal('10'), Decimal('10'), Decimal('10'), Decimal('5'), Decimal('10'), Decimal('10'))
        multipliers = (Decimal('-1'), Decimal('-1'), Decimal('-1'), Decimal('1'), Decimal('-1'), Decimal('1'))
        now.return_value = self.YOUNG_DATE + timedelta(seconds=1)
        ForwardDAO.create_buy('AAA', prices[0], numbers[0], Decimal('9000'), StrategyEnum.COUNTER_CYCLICAL)
        now.return_value = self.YOUNG_DATE + timedelta(seconds=2)
        ForwardDAO.create_buy('AAA', prices[1], numbers[1], Decimal('8000'), StrategyEnum.COUNTER_CYCLICAL)
        now.return_value = self.YOUNG_DATE + timedelta(seconds=3)
        ForwardDAO.create_buy('BBB', prices[2], numbers[2], Decimal('7000'), StrategyEnum.COUNTER_CYCLICAL)
        now.return_value = self.YOUNG_DATE + timedelta(seconds=4)
        ForwardDAO.create_sell('BBB', prices[3], numbers[3], Decimal('7500'), StrategyEnum.COUNTER_CYCLICAL)
        now.return_value = self.YOUNG_DATE + timedelta(seconds=5)
        ForwardDAO.create_buy('CCC', prices[4], numbers[4], Decimal('6500'), StrategyEnum.COUNTER_CYCLICAL)
        now.return_value = self.YOUNG_DATE + timedelta(seconds=6)
        ForwardDAO.create_sell('CCC', prices[5], numbers[5], Decimal('7500'), StrategyEnum.COUNTER_CYCLICAL)
        inventory, cash, fee = ForwardBO.init(StrategyEnum.COUNTER_CYCLICAL)
        estimated = ConfigurationEnum.FORWARD_CASH.val
        for i in range(len(prices)):
            estimated += prices[i] * numbers[i] * multipliers[i] - ConfigurationEnum.FORWARD_FEE.val
        self.assert_attributes(inventory['AAA'], price=Decimal('30'), number=Decimal('20'))
        self.assert_attributes(inventory['BBB'], price=Decimal('50'), number=Decimal('5'))
        self.assert_attributes(inventory['CCC'], price=Decimal('70'), number=ZERO)
        self.assertEqual(cash, estimated)

    def test_update(self):
        self.persist_intraday('AAA', self.YOUNG_DATE, Decimal('10'), Decimal('10'), Decimal('10'), Decimal('10'),
                              Decimal('10'))
        self.persist_intraday('AAA', self.OLD_DATE, Decimal('7'), Decimal('7'), Decimal('7'), Decimal('7'),
                              Decimal('7'))
        self.persist_intraday('BBB', self.YOUNG_DATE, Decimal('20'), Decimal('20'), Decimal('20'), Decimal('20'),
                              Decimal('20'))
        self.persist_intraday('BBB', self.OLD_DATE, Decimal('8'), Decimal('8'), Decimal('8'), Decimal('8'),
                              Decimal('8'))
        self.persist_intraday('CCC', self.YOUNG_DATE, Decimal('30'), Decimal('30'), Decimal('30'), Decimal('30'),
                              Decimal('30'))
        self.persist_intraday('CCC', self.OLD_DATE, Decimal('9'), Decimal('9'), Decimal('9'), Decimal('9'),
                              Decimal('9'))
        inventory = {
            'AAA': InventoryBO(Decimal('70'), Decimal('1')),
            'BBB': InventoryBO(Decimal('80'), Decimal('2')),
            'CCC': InventoryBO(Decimal('90'), Decimal('3')),
        }
        inventory, total_value, total = ForwardBO.update(inventory, ConfigurationEnum.FORWARD_CASH.val)
        self.assert_attributes(inventory['AAA'], price=Decimal('10'), number=Decimal('70'))
        self.assert_attributes(inventory['BBB'], price=Decimal('20'), number=Decimal('80'))
        self.assert_attributes(inventory['CCC'], price=Decimal('30'), number=Decimal('90'))
        estimated = inventory['AAA'].value() + inventory['BBB'].value() + inventory['CCC'].value()
        self.assertEqual(total_value, estimated)
        self.assertEqual(total, estimated + ConfigurationEnum.FORWARD_CASH.val)

    @patch('trading_bot.utils.utils.Utils.now')
    def test_group_by_strategy(self, now):
        dates = date_range('1/1/2000', periods=2)
        for i in range(len(dates)):
            now.return_value = self.create_datetime(dates[i])
            ForwardDAO.create_buy('AAA', Decimal(i), Decimal(i), Decimal(i), StrategyEnum.COUNTER_CYCLICAL)
            now.return_value = self.create_datetime(dates[i] + timedelta(seconds=2))
            ForwardDAO.create_buy('AAA', Decimal(i), Decimal(i), Decimal(i), StrategyEnum.VOLUME_TRADING)
        grouped = ForwardBO.group_by_strategy()
        self.assertEqual(len(grouped), 2)
        for group in grouped.values():
            self.assertEqual(len(group), 2)
        for evaluation in grouped[StrategyEnum.COUNTER_CYCLICAL]:
            self.assertEqual(evaluation.strategy, StrategyEnum.COUNTER_CYCLICAL)
        for evaluation in grouped[StrategyEnum.VOLUME_TRADING]:
            self.assertEqual(evaluation.strategy, StrategyEnum.VOLUME_TRADING)

    @patch('trading_bot.utils.utils.Utils.now')
    def test_get_account(self, now):
        dates = date_range('1/1/2000', periods=10)
        for i in range(len(dates)):
            date = self.create_datetime(dates[i])
            now.return_value = date
            self.persist_intraday('AAA', date, Decimal(i), Decimal(i), Decimal(i), Decimal(i + 1), Decimal(i))
            ForwardDAO.create_buy('AAA', Decimal(i + 1), Decimal(i + 1), Decimal(i + 1), StrategyEnum.COUNTER_CYCLICAL)
            ForwardDAO.create_buy('AAA', Decimal(i + 2), Decimal(i + 2), Decimal(i + 2), StrategyEnum.VOLUME_TRADING)
            ForwardDAO.create_buy('AAA', Decimal(i + 3), Decimal(i + 3), Decimal(i + 3), StrategyEnum.PREDICTOR)
        accounts = ForwardBO.get_accounts()
        self.assertEqual(len(accounts), len(StrategyEnum))
        for account in accounts.values():
            self.assertIsInstance(account, AccountDTO)
        account = accounts[StrategyEnum.COUNTER_CYCLICAL]
        self.assert_attributes(account, cash=Decimal('9576'), total_value=Decimal('550'), total=Decimal('10126'))
        account = accounts[StrategyEnum.VOLUME_TRADING]
        self.assert_attributes(account, cash=Decimal('9456'), total_value=Decimal('650'), total=Decimal('10106'))
        account = accounts[StrategyEnum.PREDICTOR]
        self.assert_attributes(account, cash=Decimal('9316'), total_value=Decimal('750'), total=Decimal('10066'))
