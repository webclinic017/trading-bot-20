from unittest import TestCase
from unittest.mock import patch

from src import db
from src.bo.portfolio_bo import PortfolioBO
from src.dao.portfolio_dao import PortfolioDAO
from src.dao.stock_dao import StockDAO
from src.enums.mode_enum import ModeEnum
from tests.utils.utils import Utils


class PortfolioBOTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()

    def tearDown(self):
        Utils.truncate_tables()

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_forward_portfolio(self, isin):
        PortfolioBOTestCase.__init_database(isin)
        portfolio = PortfolioBO.forward_portfolio(100)
        self.assertEqual(len(portfolio), 2)
        self.assertEqual(portfolio[0], 'ticker1')
        self.assertEqual(portfolio[1], 'ticker2')

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_backward_portfolio(self, isin):
        PortfolioBOTestCase.__init_database(isin)
        portfolio = PortfolioBO.backward_portfolio(100)
        self.assertEqual(len(portfolio), 2)
        self.assertEqual(portfolio[0], 'ticker3')
        self.assertEqual(portfolio[1], 'ticker4')

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_backward_forward_portfolio(self, isin):
        PortfolioBOTestCase.__init_database(isin)
        portfolio = PortfolioBO.backward_forward_portfolio()
        self.assertEqual(len(portfolio), 4)
        self.assertEqual(portfolio[0], 'ticker1')
        self.assertEqual(portfolio[1], 'ticker2')
        self.assertEqual(portfolio[2], 'ticker3')
        self.assertEqual(portfolio[3], 'ticker4')

    @patch('src.bo.portfolio_bo.tickers_sp500')
    def test_init(self, tickers_sp500):
        tickers_sp500.return_value = ('AAA', 'BBB', 'CCC', 'DDD')
        PortfolioBO.init()
        portfolio = PortfolioBO.forward_portfolio(100)
        self.assertEqual(len(portfolio), 4)
        self.assertEqual(portfolio[0], 'AMZN')
        self.assertEqual(portfolio[1], 'BABA')
        self.assertEqual(portfolio[2], 'MSFT')
        self.assertEqual(portfolio[3], 'GOOGL')
        portfolio = PortfolioBO.backward_portfolio(100)
        self.assertEqual(len(portfolio), 4)
        self.assertEqual(portfolio[0], 'BBB')
        self.assertEqual(portfolio[1], 'DDD')
        self.assertEqual(portfolio[2], 'CCC')
        self.assertEqual(portfolio[3], 'AAA')
        portfolio = PortfolioBO.backward_forward_portfolio()
        self.assertEqual(len(portfolio), 8)
        self.assertEqual(portfolio[0], 'AMZN')
        self.assertEqual(portfolio[1], 'BABA')
        self.assertEqual(portfolio[2], 'MSFT')
        self.assertEqual(portfolio[3], 'GOOGL')
        self.assertEqual(portfolio[4], 'BBB')
        self.assertEqual(portfolio[5], 'DDD')
        self.assertEqual(portfolio[6], 'CCC')
        self.assertEqual(portfolio[7], 'AAA')
        stocks = StockDAO.read_all()
        self.assertEqual(len(stocks), 8)
        self.assertListEqual(list(map(lambda stock: stock.ticker, stocks)), ['AAA', 'BBB', 'CCC', 'DDD',
                                                                             'BABA', 'AMZN', 'MSFT', 'GOOGL'])

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_update(self, isin):
        isin.return_value = 'isin'
        PortfolioBO.update('AAA', ModeEnum.BACKWARD)
        portfolio = PortfolioBO.read()
        self.assertEqual(len(portfolio), 1)
        Utils.assert_attributes(portfolio[0], ticker='AAA', mode=ModeEnum.BACKWARD)
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
