from unittest.mock import patch

from src import db
from src.bo.configuration_bo import ConfigurationBO
from src.bo.portfolio_bo import PortfolioBO
from src.common.database import Database
from src.enums.configuration_enum import ConfigurationEnum
from tests.base_test_case import BaseTestCase


class DatabaseTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    @patch('src.bo.portfolio_bo.tickers_sp500')
    @patch('src.bo.portfolio_bo.tickers_nasdaq')
    def test_init(self, tickers_nasdaq, tickers_sp500):
        ticker_list = ('BBB', 'DDD', 'CCC', 'AAA')
        tickers_sp500.return_value = ('AAA', 'BBB')
        tickers_nasdaq.return_value = ('CCC', 'DDD')
        Database.init()
        portfolio = PortfolioBO.forward_portfolio(100)
        self.assertEqual(len(portfolio), 4)
        for p, ticker in zip(portfolio, ticker_list):
            self.assertEqual(p, ticker)
        portfolio = PortfolioBO.backward_portfolio(100)
        self.assertEqual(len(portfolio), 4)
        for p, ticker in zip(portfolio, ticker_list):
            self.assertEqual(p, ticker)
        portfolio = PortfolioBO.backward_forward_portfolio()
        self.assertEqual(len(portfolio), 8)
        for p, ticker in zip(portfolio, ticker_list * 2):
            self.assertEqual(p, ticker)
        configurations = ConfigurationBO.read_all()
        for enum, configuration in zip(ConfigurationEnum.__iter__(), configurations):
            self.assert_attributes(configuration, identifier=enum.identifier, value=enum.val,
                                   description=enum.description)
