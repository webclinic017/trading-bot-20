import unittest
from datetime import datetime
from unittest.mock import patch

import pytz

from src import db
from src.dao.forward_dao import ForwardDAO
from src.entity.forward_entity import ForwardEntity
from src.entity.stock_entity import StockEntity
from src.enums.action_enum import ActionEnum
from tests.utils.utils import Utils


class ForwardDAOTestCase(unittest.TestCase):
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))

    @classmethod
    def setUpClass(cls):
        db.create_all()

    @patch('src.utils.utils.Utils.now')
    def setUp(self, now):
        StockEntity.query.delete()
        ForwardEntity.query.delete()
        now.return_value = ForwardDAOTestCase.YOUNG_DATE
        ForwardDAO.create_buy('AAA', 100, 4, 10)
        now.return_value = ForwardDAOTestCase.OLD_DATE
        ForwardDAO.create_sell('AAA', 101, 5, 11)

    def test_read(self):
        rows = ForwardDAO.read()
        self.assertEqual(len(rows), 2)
        Utils.assert_attributes(rows[0], timestamp=ForwardDAOTestCase.OLD_DATE, ticker='AAA', action=ActionEnum.SELL,
                                price=101, number=5, cash=11)
        Utils.assert_attributes(rows[1], timestamp=ForwardDAOTestCase.YOUNG_DATE, ticker='AAA',
                                action=ActionEnum.BUY, price=100, number=4, cash=10)

    def test_read_all(self):
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 2)

    def test_read_latest_date(self):
        latest_date = ForwardDAO.read_latest_date()
        self.assertEqual(latest_date[0], ForwardDAOTestCase.YOUNG_DATE)
