from datetime import datetime, timedelta
from decimal import Decimal
from json import dumps
from unittest.mock import patch

import pytz

from src import db
from src.bo.configuration_bo import ConfigurationBO
from src.bo.forward_bo import ForwardBO
from src.bo.inventory_bo import InventoryBO
from src.common.constants import ZERO
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dto.attempt_dto import AttemptDTO
from src.enums.action_enum import ActionEnum
from src.enums.configuration_enum import ConfigurationEnum
from tests.base_test_case import BaseTestCase


class ForwardBOTestCase(BaseTestCase):
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))
    STATISTIC_JSON = [{
        "action": "ActionEnum.SELL",
        "date": "2000-05-29 04:00:00+00:00",
        "price": "500.0000000000",
        "ticker": "AAA"}, {
        "action": "ActionEnum.BUY",
        "date": "2000-05-29 04:00:00+00:00",
        "price": "100.0000000000",
        "ticker": "CCC"}]

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()
        ConfigurationBO.init()

    @patch('src.utils.utils.Utils.send_mail')
    @patch('src.utils.utils.Utils.is_today')
    @patch('src.utils.utils.Utils.is_working_day_ny')
    @patch('src.utils.utils.Utils.now')
    def test_start(self, now, is_working_day_ny, is_today, send_mail):
        is_today.return_value = False
        is_working_day_ny.return_value = True
        now.return_value = self.OLD_DATE
        ForwardDAO.create_buy('AAA', Decimal('100'), Decimal('10'), Decimal('8996.1'))
        ForwardDAO.create_buy('BBB', Decimal('100'), Decimal('10'), Decimal('7992.200000000001'))
        now.return_value = self.YOUNG_DATE
        EvaluationDAO.create(Decimal('40000'), '', AttemptDTO())
        self.persist_intraday_frame()
        ForwardBO.start(['AAA', 'BBB', 'CCC'])
        send_mail.assert_called_with(dumps(self.STATISTIC_JSON, indent=4, sort_keys=True, default=str))
        self.assertEqual(send_mail.call_count, 1)
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 4)
        self.assert_attributes(rows[0], action=ActionEnum.BUY, cash=Decimal('8996.1'), timestamp=self.OLD_DATE,
                               number=Decimal('10'), price=Decimal('100'), ticker='AAA')
        self.assert_attributes(rows[1], action=ActionEnum.BUY, cash=Decimal('7992.2'), timestamp=self.OLD_DATE,
                               number=Decimal('10'), price=Decimal('100'), ticker='BBB')
        self.assert_attributes(rows[2], action=ActionEnum.SELL, cash=Decimal('8988.3'), timestamp=self.YOUNG_DATE,
                               number=Decimal('2'), price=Decimal('500'), ticker='AAA')
        self.assert_attributes(rows[3], action=ActionEnum.BUY, cash=Decimal('7984.4'), timestamp=self.YOUNG_DATE,
                               number=Decimal('10'), price=Decimal('100'), ticker='CCC')

    @patch('src.utils.utils.Utils.now')
    def test_init(self, now):
        prices = (Decimal('20'), Decimal('30'), Decimal('40'), Decimal('50'), Decimal('60'), Decimal('70'))
        numbers = (Decimal('10'), Decimal('10'), Decimal('10'), Decimal('5'), Decimal('10'), Decimal('10'))
        multipliers = (Decimal('-1'), Decimal('-1'), Decimal('-1'), Decimal('1'), Decimal('-1'), Decimal('1'))
        now.return_value = self.YOUNG_DATE + timedelta(seconds=1)
        ForwardDAO.create_buy('AAA', prices[0], numbers[0], Decimal('9000'))
        now.return_value = self.YOUNG_DATE + timedelta(seconds=2)
        ForwardDAO.create_buy('AAA', prices[1], numbers[1], Decimal('8000'))
        now.return_value = self.YOUNG_DATE + timedelta(seconds=3)
        ForwardDAO.create_buy('BBB', prices[2], numbers[2], Decimal('7000'))
        now.return_value = self.YOUNG_DATE + timedelta(seconds=4)
        ForwardDAO.create_sell('BBB', prices[3], numbers[3], Decimal('7500'))
        now.return_value = self.YOUNG_DATE + timedelta(seconds=5)
        ForwardDAO.create_buy('CCC', prices[4], numbers[4], Decimal('6500'))
        now.return_value = self.YOUNG_DATE + timedelta(seconds=6)
        ForwardDAO.create_sell('CCC', prices[5], numbers[5], Decimal('7500'))
        inventory, cash, fee = ForwardBO.init()
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
