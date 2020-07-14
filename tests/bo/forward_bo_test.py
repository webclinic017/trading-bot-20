import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import pytz

from src import db
from src.bo.forward_bo import ForwardBO
from src.bo.inventory_bo import InventoryBO
from src.constants import INITIAL_CASH, FEE
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dto.attempt_dto import AttemptDTO
from src.enums.action_enum import ActionEnum
from tests.utils.utils import Utils


class ForwardBOTestCase(unittest.TestCase):
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()

    @patch('src.utils.utils.Utils.is_today')
    @patch('src.utils.utils.Utils.is_working_day_ny')
    @patch('src.utils.utils.Utils.now')
    def test_start(self, now, is_working_day_ny, is_today):
        is_today.return_value = False
        is_working_day_ny.return_value = True
        now.return_value = ForwardBOTestCase.OLD_DATE
        ForwardDAO.create_buy('AAA', 100.0, 10, 8996.1)
        ForwardDAO.create_buy('BBB', 100.0, 10, 7992.200000000001)
        now.return_value = ForwardBOTestCase.YOUNG_DATE
        EvaluationDAO.create(40000, '', AttemptDTO())
        Utils.persist_intraday_frame()
        ForwardBO.start()
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 4)
        Utils.assert_attributes(rows[0], action=ActionEnum.BUY, cash=8996.1, timestamp=ForwardBOTestCase.OLD_DATE,
                                number=10, price=100.0, ticker='AAA')
        Utils.assert_attributes(rows[1], action=ActionEnum.BUY, cash=7992.200000000001,
                                timestamp=ForwardBOTestCase.OLD_DATE, number=10, price=100.0, ticker='BBB')
        Utils.assert_attributes(rows[2], action=ActionEnum.SELL, cash=8988.300000000001,
                                timestamp=ForwardBOTestCase.YOUNG_DATE,
                                number=2, price=500.0, ticker='AAA')
        Utils.assert_attributes(rows[3], action=ActionEnum.BUY, cash=7984.4000000000015,
                                timestamp=ForwardBOTestCase.YOUNG_DATE,
                                number=10, price=100.0, ticker='CCC')

    @patch('src.utils.utils.Utils.now')
    def test_init(self, now):
        prices = (20, 30, 40, 50, 60, 70)
        numbers = (10, 10, 10, 5, 10, 10)
        multipliers = (-1, -1, -1, 1, -1, 1)
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=1)
        ForwardDAO.create_buy('AAA', prices[0], numbers[0], 9000)
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=2)
        ForwardDAO.create_buy('AAA', prices[1], numbers[1], 8000)
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=3)
        ForwardDAO.create_buy('BBB', prices[2], numbers[2], 7000)
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=4)
        ForwardDAO.create_sell('BBB', prices[3], numbers[3], 7500)
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=5)
        ForwardDAO.create_buy('CCC', prices[4], numbers[4], 6500)
        now.return_value = ForwardBOTestCase.YOUNG_DATE + timedelta(seconds=6)
        ForwardDAO.create_sell('CCC', prices[5], numbers[5], 7500)
        inventory, cash = ForwardBO.init()
        estimated = INITIAL_CASH
        for i in range(len(prices)):
            estimated += prices[i] * numbers[i] * multipliers[i] - FEE
        Utils.assert_attributes(inventory['AAA'], price=30.0, number=20)
        Utils.assert_attributes(inventory['BBB'], price=50.0, number=5)
        Utils.assert_attributes(inventory['CCC'], price=70.0, number=0)
        self.assertEqual(cash, estimated)

    def test_update(self):
        Utils.persist_intraday('AAA', ForwardBOTestCase.YOUNG_DATE, 10, 10, 10, 10, 10)
        Utils.persist_intraday('AAA', ForwardBOTestCase.OLD_DATE, 7, 7, 7, 7, 7)
        Utils.persist_intraday('BBB', ForwardBOTestCase.YOUNG_DATE, 20, 20, 20, 20, 20)
        Utils.persist_intraday('BBB', ForwardBOTestCase.OLD_DATE, 8, 8, 8, 8, 8)
        Utils.persist_intraday('CCC', ForwardBOTestCase.YOUNG_DATE, 30, 30, 30, 30, 30)
        Utils.persist_intraday('CCC', ForwardBOTestCase.OLD_DATE, 9, 9, 9, 9, 9)
        inventory = {
            'AAA': InventoryBO(70, 1),
            'BBB': InventoryBO(80, 2),
            'CCC': InventoryBO(90, 3),
        }
        inventory, total_value, total = ForwardBO.update(inventory, INITIAL_CASH)
        Utils.assert_attributes(inventory['AAA'], price=10, number=70)
        Utils.assert_attributes(inventory['BBB'], price=20, number=80)
        Utils.assert_attributes(inventory['CCC'], price=30, number=90)
        estimated = inventory['AAA'].value() + inventory['BBB'].value() + inventory['CCC'].value()
        self.assertEqual(total_value, estimated)
        self.assertEqual(total, estimated + INITIAL_CASH)


if __name__ == '__main__':
    unittest.main()
