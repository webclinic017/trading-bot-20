from unittest import TestCase
from unittest.mock import patch

from src import db
from src.dao.portfolio_dao import PortfolioDAO
from src.dao.stock_dao import StockDAO
from src.entity.portfolio_entity import PortfolioEntity
from src.enums.mode_enum import ModeEnum
from tests.utils.utils import Utils


class PortfolioDAOTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()

    @patch('src.bo.stock_bo.StockBO.isin')
    def test_read_all(self, isin):
        Utils.truncate_tables()
        isin.return_value = 'isin'
        StockDAO.update(('ticker1', 'ticker2', 'ticker3',))
        PortfolioDAO.create('ticker1', ModeEnum.FORWARD)
        PortfolioDAO.create('ticker2', ModeEnum.BACKWARD)
        portfolio = PortfolioDAO.read()
        Utils.assert_attributes(portfolio[0], ticker='ticker1', mode=ModeEnum.FORWARD, isin='isin')
        Utils.assert_attributes(portfolio[1], ticker='ticker2', mode=ModeEnum.BACKWARD, isin='isin')

    def test_read_filter_by_ticker(self):
        PortfolioDAO.update('ticker1', ModeEnum.BACKWARD)
        portfolio = PortfolioDAO.read_filter_by_ticker('ticker1')
        self.assertIsInstance(portfolio, PortfolioEntity)
        Utils.assert_attributes(portfolio, ticker='ticker1', mode=ModeEnum.BACKWARD)

    def test_update(self):
        PortfolioDAO.update('ticker1', ModeEnum.BACKWARD)
        portfolio = PortfolioDAO.read_filter_by_ticker('ticker1')
        self.assertIsInstance(portfolio, PortfolioEntity)
        Utils.assert_attributes(portfolio, ticker='ticker1', mode=ModeEnum.BACKWARD)

        PortfolioDAO.update('ticker3', ModeEnum.FORWARD)
        PortfolioDAO.update('ticker3', ModeEnum.BACKWARD)
        portfolio = PortfolioDAO.read_filter_by_ticker('ticker3')
        self.assertIsInstance(portfolio, PortfolioEntity)
        Utils.assert_attributes(portfolio, ticker='ticker3', mode=ModeEnum.BACKWARD)
