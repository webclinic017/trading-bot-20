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

    def setUp(self):
        StockEntity.query.delete()

    @patch('src.utils.Utils.now')
    def test_read_latest_date(self, now):
        latest_date = ForwardDAO.read_latest_date()
        self.assertEqual(latest_date, (None,))
        self.assertEqual(latest_date[0], None)
        now.return_value = datetime.fromisoformat('2011-11-05T00:00:00')
        ForwardDAO.create_buy('AAA', 100, 4, 10)
        now.return_value = datetime.fromisoformat('2011-11-04T00:00:00')
        ForwardDAO.create_buy('AAA', 100, 4, 10)
        latest_date = ForwardDAO.read_latest_date()
        self.assertEqual(latest_date[0], datetime.fromisoformat('2011-11-05T00:00:00'))
