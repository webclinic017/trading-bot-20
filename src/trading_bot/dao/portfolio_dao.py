from typing import List, Any

from sqlalchemy.exc import OperationalError

from trading_bot import db
from trading_bot.dao.base_dao import BaseDAO
from trading_bot.entity.portfolio_entity import PortfolioEntity
from trading_bot.entity.stock_entity import StockEntity
from trading_bot.enums.mode_enum import ModeEnum
from trading_bot.utils.utils import Utils


class PortfolioDAO(BaseDAO):

    @classmethod
    def create(cls, symbol: str, mode: ModeEnum) -> None:
        portfolio: PortfolioEntity = PortfolioEntity()
        Utils.set_attributes(portfolio, symbol=symbol, mode=mode)
        cls.persist(portfolio)

    @staticmethod
    def read() -> List[Any]:
        return db.session.query(PortfolioEntity.symbol, PortfolioEntity.mode, StockEntity.isin).join(
            StockEntity, StockEntity.symbol == PortfolioEntity.symbol).all()

    @staticmethod
    def read_filter_by_symbol_isin(symbol: str) -> Any:
        return db.session.query(PortfolioEntity.symbol, PortfolioEntity.mode, StockEntity.isin).filter(
            StockEntity.symbol == symbol).join(StockEntity, StockEntity.symbol == PortfolioEntity.symbol).first()

    @staticmethod
    def read_filter_by_symbol(symbol: str) -> PortfolioEntity:
        return PortfolioEntity.query.filter_by(symbol=symbol).first()

    @staticmethod
    def read_filter_by_mode(mode: ModeEnum) -> List[PortfolioEntity]:
        try:
            return PortfolioEntity.query.filter_by(mode=mode).all()
        except OperationalError:
            return []

    @classmethod
    def update(cls, symbol: str, mode: ModeEnum) -> None:
        portfolio = cls.read_filter_by_symbol(symbol)
        if portfolio is None:
            cls.create(symbol, mode)
        else:
            portfolio.mode = mode
            cls.commit()

    @classmethod
    def delete(cls, symbol: str) -> None:
        PortfolioEntity.query.filter(PortfolioEntity.symbol == symbol).delete()
        cls.commit()
