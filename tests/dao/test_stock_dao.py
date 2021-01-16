from unittest.mock import patch

from src import db
from src.dao.stock_dao import StockDAO
from tests.base_test_case import BaseTestCase


class StockDAOTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_read_all(self, isin):
        isin.return_value = 'isin'
        StockDAO.update(('AAPL',))
        result = StockDAO.read_all()
        self.assertEqual(result[0].ticker, 'AAPL')
        self.assertEqual(result[0].isin, 'isin')

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_read_ticker(self, isin):
        isin.return_value = 'isin'
        portfolio = ('AAPL',)
        StockDAO.create_if_not_exists(portfolio)
        result = StockDAO.read_ticker()
        self.assertEqual(result[0].ticker, 'AAPL')

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_exception(self, isin):
        isin.return_value = 'isin'
        StockDAO.update((None,))
        result = StockDAO.read_all()
        self.assertListEqual(result, [])
