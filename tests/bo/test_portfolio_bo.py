from unittest.mock import patch

from src import db
from src.bo.portfolio_bo import PortfolioBO
from src.dao.portfolio_dao import PortfolioDAO
from src.dao.stock_dao import StockDAO
from src.enums.mode_enum import ModeEnum
from tests.base_test_case import BaseTestCase


class PortfolioBOTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()

    def tearDown(self):
        self.truncate_tables()

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_forward_portfolio(self, isin):
        self.__init_database(isin)
        portfolio = PortfolioBO.forward_portfolio(100)
        self.assertEqual(len(portfolio), 2)
        self.assertEqual(portfolio[0], 'ticker1')
        self.assertEqual(portfolio[1], 'ticker2')

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_backward_portfolio(self, isin):
        self.__init_database(isin)
        portfolio = PortfolioBO.backward_portfolio(100)
        self.assertEqual(len(portfolio), 2)
        self.assertEqual(portfolio[0], 'ticker3')
        self.assertEqual(portfolio[1], 'ticker4')

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_backward_forward_portfolio(self, isin):
        self.__init_database(isin)
        portfolio = PortfolioBO.backward_forward_portfolio()
        self.assertEqual(len(portfolio), 4)
        self.assertEqual(portfolio[0], 'ticker1')
        self.assertEqual(portfolio[1], 'ticker2')
        self.assertEqual(portfolio[2], 'ticker3')
        self.assertEqual(portfolio[3], 'ticker4')

    @patch('src.bo.portfolio_bo.tickers_sp500')
    @patch('src.bo.portfolio_bo.tickers_nasdaq')
    @patch('src.dao.stock_dao.StockDAO.update')
    def test_init(self, update, tickers_nasdaq, tickers_sp500):
        ticker_list = ('FFF', 'BBB', 'DDD', 'GGG', 'CCC', 'AAA', 'HHH', 'EEE')
        tickers_sp500.return_value = ('AAA', 'BBB', 'CCC', 'DDD')
        tickers_nasdaq.return_value = ('EEE', 'FFF', 'GGG', 'HHH')
        PortfolioBO.init()
        portfolio = PortfolioBO.forward_portfolio(100)
        self.assertEqual(len(portfolio), 8)
        for p, ticker in zip(portfolio, ticker_list):
            self.assertEqual(p, ticker)
        portfolio = PortfolioBO.backward_portfolio(100)
        self.assertEqual(len(portfolio), 8)
        for p, ticker in zip(portfolio, ticker_list):
            self.assertEqual(p, ticker)
        portfolio = PortfolioBO.backward_forward_portfolio()
        self.assertEqual(len(portfolio), 16)
        for p, ticker in zip(portfolio, ticker_list * 2):
            self.assertEqual(p, ticker)
        update.assert_called_once_with(tuple(sorted(ticker_list)))

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_update(self, isin):
        isin.return_value = 'isin'
        PortfolioBO.update('AAA', ModeEnum.BACKWARD)
        portfolio = PortfolioBO.read()
        self.assertEqual(len(portfolio), 1)
        self.assert_attributes(portfolio[0], ticker='AAA', mode=ModeEnum.BACKWARD)
        PortfolioBO.delete('AAA')
        portfolio = PortfolioBO.read_filter_by_ticker_isin('AAA')
        self.assertIsNone(portfolio)

    @staticmethod
    def __init_database(isin):
        isin.return_value = 'isin'
        StockDAO.update(('ticker1', 'ticker2', 'ticker3', 'ticker4',))
        PortfolioDAO.create('ticker1', ModeEnum.FORWARD)
        PortfolioDAO.create('ticker2', ModeEnum.FORWARD)
        PortfolioDAO.create('ticker3', ModeEnum.BACKWARD)
        PortfolioDAO.create('ticker4', ModeEnum.BACKWARD)
