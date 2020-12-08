from unittest import TestCase
from unittest.mock import patch

from src import db
from src.bo.configuration_bo import ConfigurationBO
from src.bo.portfolio_bo import PortfolioBO
from src.database import Database
from src.enums.configuration_enum import ConfigurationEnum
from tests.utils.utils import Utils


class DatabaseTestCase(TestCase):
    TICKER = ('CCC', 'DDD')

    @classmethod
    def setUpClass(cls):
        db.create_all()

    @patch('src.bo.portfolio_bo.tickers_sp500')
    @patch('src.bo.portfolio_bo.PortfolioBO.FORWARD_TICKER', new=TICKER)
    def test_init(self, tickers_sp500):
        tickers_sp500.return_value = ('AAA', 'BBB')
        Database.init()
        portfolio = PortfolioBO.forward_portfolio(100)
        self.assertEqual(len(portfolio), 2)
        self.assertEqual(portfolio[0], 'DDD')
        self.assertEqual(portfolio[1], 'CCC')
        portfolio = PortfolioBO.backward_portfolio(100)
        self.assertEqual(len(portfolio), 2)
        self.assertEqual(portfolio[0], 'BBB')
        self.assertEqual(portfolio[1], 'AAA')
        portfolio = PortfolioBO.backward_forward_portfolio()
        self.assertEqual(len(portfolio), 4)
        self.assertEqual(portfolio[0], 'DDD')
        self.assertEqual(portfolio[1], 'CCC')
        self.assertEqual(portfolio[2], 'BBB')
        self.assertEqual(portfolio[3], 'AAA')
        configurations = ConfigurationBO.read_all()
        for enum, configuration in zip(ConfigurationEnum.__iter__(), configurations):
            Utils.assert_attributes(configuration, identifier=enum.identifier, value=enum.val,
                                    description=enum.description)
