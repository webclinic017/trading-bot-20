from unittest.mock import patch

from tests.base_test_case import BaseTestCase
from trading_bot import db
from trading_bot.dao.stock_dao import StockDAO


class StockDAOTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()

    @patch('trading_bot.bo.stock_bo.StockBO.isin')
    def test_read_all(self, isin):
        isin.return_value = 'isin'
        StockDAO.update(lambda: ['AAA', ])
        result = StockDAO.read_all()
        self.assertEqual(result[0].symbol, 'AAA')
        self.assertEqual(result[0].isin, 'isin')

    @patch('trading_bot.bo.stock_bo.StockBO.isin')
    def test_read_symbol(self, isin):
        isin.return_value = 'isin'
        portfolio = ['AAA', ]
        StockDAO.create_if_not_exists(portfolio)
        result = StockDAO.read_symbol()
        self.assertEqual(result[0].symbol, 'AAA')

    @patch('trading_bot.bo.stock_bo.StockBO.isin')
    def test_exception(self, isin):
        isin.return_value = 'isin'
        StockDAO.update(lambda: [None, ])
        result = StockDAO.read_all()
        self.assertListEqual(result, [])
