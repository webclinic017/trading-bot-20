import unittest
from unittest.mock import patch

from src import db
from src.dao.stock_dao import StockDAO
from src.entity.stock_entity import StockEntity


class StockDAOTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        StockEntity.query.delete()

    @patch('src.isin.Isin.isin')
    def test_read_all(self, isin):
        isin.return_value = 'isin'
        StockDAO.update('AAPL')
        result = StockDAO.read_all()
        self.assertEqual(result[0].ticker, 'AAPL')
        self.assertEqual(result[0].isin, 'isin')

    @patch('src.isin.Isin.isin')
    def test_read_ticker(self, isin):
        isin.return_value = 'isin'
        portfolio = ('AAPL',)
        StockDAO.create_if_not_exists(portfolio)
        result = StockDAO.read_ticker()
        self.assertEqual(result[0].ticker, 'AAPL')


if __name__ == '__main__':
    unittest.main()
