from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

import pytz

from src import db
from src.dao.forward_dao import ForwardDAO
from src.enums.action_enum import ActionEnum
from tests.utils.utils import Utils


class ForwardDAOTestCase(TestCase):
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))

    @classmethod
    def setUpClass(cls):
        db.create_all()

    @patch('src.utils.utils.Utils.now')
    def setUp(self, now):
        Utils.truncate_tables()
        now.return_value = ForwardDAOTestCase.YOUNG_DATE
        ForwardDAO.create_buy('AAA', Decimal('100'), Decimal('4'), Decimal('10'))
        now.return_value = ForwardDAOTestCase.OLD_DATE
        ForwardDAO.create_sell('AAA', Decimal('101'), Decimal('5'), Decimal('11'))

    def test_read(self):
        rows = ForwardDAO.read()
        self.assertEqual(len(rows), 2)
        Utils.assert_attributes(rows[0], timestamp=ForwardDAOTestCase.OLD_DATE, ticker='AAA', action=ActionEnum.SELL,
                                price=Decimal('101'), number=Decimal('5'), cash=Decimal('11'))
        Utils.assert_attributes(rows[1], timestamp=ForwardDAOTestCase.YOUNG_DATE, ticker='AAA', action=ActionEnum.BUY,
                                price=Decimal('100'), number=Decimal('4'), cash=Decimal('10'))

    def test_read_all(self):
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 2)

    def test_read_latest_date(self):
        latest_date = ForwardDAO.read_latest_date()
        self.assertEqual(latest_date, ForwardDAOTestCase.YOUNG_DATE)
