import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch

import pytz

from src import db
from src.bo.configuration_bo import ConfigurationBO
from src.bo.forward_bo import ForwardBO
from src.bo.inventory_bo import InventoryBO
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dto.attempt_dto import AttemptDTO
from src.enums.action_enum import ActionEnum
from src.enums.configuration_enum import ConfigurationEnum
from tests.utils.utils import Utils


class ForwardBOTestCase(unittest.TestCase):
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()
        ConfigurationBO.create()

    @patch('src.utils.utils.Utils.is_today')
    @patch('src.utils.utils.Utils.is_working_day_ny')
    @patch('src.utils.utils.Utils.now')
    def test_start(self, now, is_working_day_ny, is_today):
        is_today.return_value = False
        is_working_day_ny.return_value = True
        now.return_value = ForwardBOTestCase.OLD_DATE
        ForwardDAO.create_buy('AAA', Decimal('100'), Decimal('10'), Decimal('8996.1'))
        ForwardDAO.create_buy('BBB', Decimal('100'), Decimal('10'), Decimal('7992.200000000001'))
        now.return_value = ForwardBOTestCase.YOUNG_DATE
        EvaluationDAO.create(Decimal('40000'), '', AttemptDTO())
        Utils.persist_intraday_frame()
        ForwardBO.start()
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 4)
        Utils.assert_attributes(rows[0], action=ActionEnum.BUY, cash=Decimal('8996.1'),
                                timestamp=ForwardBOTestCase.OLD_DATE, number=Decimal('10'), price=Decimal('100'),
                                ticker='AAA')
        Utils.assert_attributes(rows[1], action=ActionEnum.BUY, cash=Decimal('7992.2'),
                                timestamp=ForwardBOTestCase.OLD_DATE, number=Decimal('10'), price=Decimal('100'),
                                ticker='BBB')
        Utils.assert_attributes(rows[2], action=ActionEnum.SELL, cash=Decimal('8988.3'),
                                timestamp=ForwardBOTestCase.YOUNG_DATE,
                                number=Decimal('2'), price=Decimal('500'), ticker='AAA')
        Utils.assert_attributes(rows[3], action=ActionEnum.BUY, cash=Decimal('7984.4'),
                                timestamp=ForwardBOTestCase.YOUNG_DATE,
                                number=Decimal('10'), price=Decimal('100'), ticker='CCC')

    @patch('src.utils.utils.Utils.now')
    def test_init(self, now):
        prices = (Decimal('20'), Decimal('30'), Decimal('40'), Decimal('50'), Decimal('60'), Decimal('70'))
        numbers = (Decimal('10'), Decimal('10'), Decimal('10'), Decimal('5'), Decimal('10'), Decimal('10'))
        multipliers = (Decimal('-1'), Decimal('-1'), Decimal('-1'), Decimal('1'), Decimal('-1'), Decimal('1'))
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=1)
        ForwardDAO.create_buy('AAA', prices[0], numbers[0], Decimal('9000'))
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=2)
        ForwardDAO.create_buy('AAA', prices[1], numbers[1], Decimal('8000'))
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=3)
        ForwardDAO.create_buy('BBB', prices[2], numbers[2], Decimal('7000'))
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=4)
        ForwardDAO.create_sell('BBB', prices[3], numbers[3], Decimal('7500'))
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=5)
        ForwardDAO.create_buy('CCC', prices[4], numbers[4], Decimal('6500'))
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=6)
        ForwardDAO.create_sell('CCC', prices[5], numbers[5], Decimal('7500'))
        inventory, cash, fee = ForwardBO.init()
        estimated = ConfigurationEnum.FORWARD_CASH.v
        for i in range(len(prices)):
            estimated += prices[i] * numbers[i] * multipliers[i] - ConfigurationEnum.FORWARD_FEE.v
        Utils.assert_attributes(inventory['AAA'], price=Decimal('30'), number=Decimal('20'))
        Utils.assert_attributes(inventory['BBB'], price=Decimal('50'), number=Decimal('5'))
        Utils.assert_attributes(inventory['CCC'], price=Decimal('70'), number=Decimal('0'))
        self.assertEqual(cash, estimated)

    def test_update(self):
        Utils.persist_intraday('AAA', ForwardBOTestCase.YOUNG_DATE, Decimal('10'), Decimal('10'), Decimal('10'),
                               Decimal('10'), Decimal('10'))
        Utils.persist_intraday('AAA', ForwardBOTestCase.OLD_DATE, Decimal('7'), Decimal('7'), Decimal('7'),
                               Decimal('7'), Decimal('7'))
        Utils.persist_intraday('BBB', ForwardBOTestCase.YOUNG_DATE, Decimal('20'), Decimal('20'), Decimal('20'),
                               Decimal('20'), Decimal('20'))
        Utils.persist_intraday('BBB', ForwardBOTestCase.OLD_DATE, Decimal('8'), Decimal('8'), Decimal('8'),
                               Decimal('8'), Decimal('8'))
        Utils.persist_intraday('CCC', ForwardBOTestCase.YOUNG_DATE, Decimal('30'), Decimal('30'), Decimal('30'),
                               Decimal('30'), Decimal('30'))
        Utils.persist_intraday('CCC', ForwardBOTestCase.OLD_DATE, Decimal('9'), Decimal('9'), Decimal('9'),
                               Decimal('9'), Decimal('9'))
        inventory = {
            'AAA': InventoryBO(Decimal('70'), Decimal('1')),
            'BBB': InventoryBO(Decimal('80'), Decimal('2')),
            'CCC': InventoryBO(Decimal('90'), Decimal('3')),
        }
        inventory, total_value, total = ForwardBO.update(inventory, ConfigurationEnum.FORWARD_CASH.v)
        Utils.assert_attributes(inventory['AAA'], price=Decimal('10'), number=Decimal('70'))
        Utils.assert_attributes(inventory['BBB'], price=Decimal('20'), number=Decimal('80'))
        Utils.assert_attributes(inventory['CCC'], price=Decimal('30'), number=Decimal('90'))
        estimated = inventory['AAA'].value() + inventory['BBB'].value() + inventory['CCC'].value()
        self.assertEqual(total_value, estimated)
        self.assertEqual(total, estimated + ConfigurationEnum.FORWARD_CASH.v)


if __name__ == '__main__':
    unittest.main()
