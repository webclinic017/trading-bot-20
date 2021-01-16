from typing import List, Any, NoReturn

from sqlalchemy.exc import OperationalError

from src import db
from src.dao.base_dao import BaseDAO
from src.entity.portfolio_entity import PortfolioEntity
from src.entity.stock_entity import StockEntity
from src.enums.mode_enum import ModeEnum
from src.utils.utils import Utils


class PortfolioDAO(BaseDAO):

    @classmethod
    def create(cls, ticker: str, mode: ModeEnum) -> NoReturn:
        portfolio: PortfolioEntity = PortfolioEntity()
        Utils.set_attributes(portfolio, ticker=ticker, mode=mode)
        cls.persist(portfolio)

    @staticmethod
    def read() -> List[Any]:
        return db.session.query(PortfolioEntity.ticker, PortfolioEntity.mode, StockEntity.isin).join(
            StockEntity, StockEntity.ticker == PortfolioEntity.ticker).all()

    @staticmethod
    def read_filter_by_ticker_isin(ticker: str) -> Any:
        return db.session.query(PortfolioEntity.ticker, PortfolioEntity.mode, StockEntity.isin).filter(
            StockEntity.ticker == ticker).join(StockEntity, StockEntity.ticker == PortfolioEntity.ticker).first()

    @staticmethod
    def read_filter_by_ticker(ticker: str) -> PortfolioEntity:
        return PortfolioEntity.query.filter_by(ticker=ticker).first()

    @staticmethod
    def read_filter_by_mode(mode: ModeEnum) -> List[PortfolioEntity]:
        try:
            return PortfolioEntity.query.filter_by(mode=mode).all()
        except OperationalError:
            return []

    @classmethod
    def update(cls, ticker: str, mode: ModeEnum) -> NoReturn:
        portfolio = cls.read_filter_by_ticker(ticker)
        if portfolio is None:
            cls.create(ticker, mode)
        else:
            portfolio.mode = mode
            cls.commit()

    @classmethod
    def delete(cls, ticker: str) -> NoReturn:
        PortfolioEntity.query.filter(PortfolioEntity.ticker == ticker).delete()
        cls.commit()
