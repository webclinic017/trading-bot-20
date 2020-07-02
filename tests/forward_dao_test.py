import unittest
from datetime import datetime
from unittest.mock import patch

from src import db
from src.dao.forward_dao import ForwardDAO
from src.entity.stock_entity import StockEntity


class ForwardDAOTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    @patch('src.utils.Utils.now')
    def setUp(self, now):
        StockEntity.query.delete()
        now.return_value = datetime.fromisoformat('2011-11-05T00:00:00')
        ForwardDAO.create_buy('AAA', 100, 4, 10)
        now.return_value = datetime.fromisoformat('2011-11-04T00:00:00')
        ForwardDAO.create_sell('AAA', 100, 4, 10)

    def test_read(self):
        rows = ForwardDAO.read()
        self.assertEqual(rows[0].date, datetime.fromisoformat('2011-11-04T00:00:00'))
        self.assertEqual(rows[1].date, datetime.fromisoformat('2011-11-05T00:00:00'))

    def test_read_all(self):
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 2)

    def test_read_latest_date(self):
        latest_date = ForwardDAO.read_latest_date()
        self.assertEqual(latest_date[0], datetime.fromisoformat('2011-11-05T00:00:00'))
