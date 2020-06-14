from src.dao.dao import DAO
from src.entity.stock_entity import StockEntity
from src.isin import Isin


class StockDAO:
    @staticmethod
    def create_if_not_exists(portfolio):
        rows = StockEntity.query.with_entities(StockEntity.ticker).filter(StockEntity.ticker.in_(portfolio)).all()
        if len(rows) < len(portfolio):
            StockDAO.update(*portfolio)

    @staticmethod
    def read_all():
        return StockEntity.query.all()

    @staticmethod
    def read_ticker():
        return StockEntity.query.with_entities(StockEntity.ticker).all()

    @staticmethod
    def update(*portfolio):
        for ticker in portfolio:
            stock = StockEntity()
            stock.ticker = ticker
            stock.isin = Isin.isin(ticker)
            DAO.persist(stock)
