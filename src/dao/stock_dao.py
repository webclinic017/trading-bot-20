from typing import Tuple, List, Union, NoReturn

from src.bo.stock_bo import StockBO
from src.dao.dao import DAO
from src.entity.stock_entity import StockEntity
from src.utils.utils import Utils


class StockDAO:
    @staticmethod
    def create_if_not_exists(portfolio: Tuple[str]) -> NoReturn:
        rows: List[StockEntity] = StockEntity.query.with_entities(StockEntity.ticker).filter(
            StockEntity.ticker.in_(portfolio)).all()
        if len(rows) < len(portfolio):
            StockDAO.update(portfolio)

    @staticmethod
    def read_all() -> List[StockEntity]:
        return StockEntity.query.all()

    @staticmethod
    def read_ticker() -> List[StockEntity]:
        return StockEntity.query.with_entities(StockEntity.ticker).all()

    @staticmethod
    def update(portfolio: Tuple[Union[str, None], ...]) -> NoReturn:
        for ticker in portfolio:
            stock: StockEntity = StockEntity()
            Utils.set_attributes(stock, ticker=ticker, isin=StockBO.isin(ticker))
            DAO.persist(stock)
