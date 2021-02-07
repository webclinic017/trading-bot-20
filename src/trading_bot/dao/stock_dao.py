from typing import Tuple, List, Union

from trading_bot.bo.stock_bo import StockBO
from trading_bot.dao.base_dao import BaseDAO
from trading_bot.entity.stock_entity import StockEntity
from trading_bot.utils.utils import Utils


class StockDAO(BaseDAO):

    @classmethod
    def create_if_not_exists(cls, portfolio: Tuple[str]) -> None:
        rows: List[StockEntity] = StockEntity.query.with_entities(StockEntity.symbol).filter(
            StockEntity.symbol.in_(portfolio)).all()
        if len(rows) < len(portfolio):
            cls.update(portfolio)

    @staticmethod
    def read_all() -> List[StockEntity]:
        return StockEntity.query.all()

    @staticmethod
    def read_symbol() -> List[StockEntity]:
        return StockEntity.query.with_entities(StockEntity.symbol).all()

    @classmethod
    def update(cls, portfolio: Tuple[Union[str, None], ...]) -> None:
        for symbol in portfolio:
            stock: StockEntity = StockEntity()
            Utils.set_attributes(stock, symbol=symbol, isin=StockBO.isin(symbol))
            cls.persist(stock)
