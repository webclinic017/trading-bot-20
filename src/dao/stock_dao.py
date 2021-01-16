from typing import Tuple, List, Union, NoReturn

from src.bo.stock_bo import StockBO
from src.dao.base_dao import BaseDAO
from src.entity.stock_entity import StockEntity
from src.utils.utils import Utils


class StockDAO(BaseDAO):

    @classmethod
    def create_if_not_exists(cls, portfolio: Tuple[str]) -> NoReturn:
        rows: List[StockEntity] = StockEntity.query.with_entities(StockEntity.ticker).filter(
            StockEntity.ticker.in_(portfolio)).all()
        if len(rows) < len(portfolio):
            cls.update(portfolio)

    @staticmethod
    def read_all() -> List[StockEntity]:
        return StockEntity.query.all()

    @staticmethod
    def read_ticker() -> List[StockEntity]:
        return StockEntity.query.with_entities(StockEntity.ticker).all()

    @classmethod
    def update(cls, portfolio: Tuple[Union[str, None], ...]) -> NoReturn:
        for ticker in portfolio:
            stock: StockEntity = StockEntity()
            Utils.set_attributes(stock, ticker=ticker, isin=StockBO.isin(ticker))
            cls.persist(stock)
