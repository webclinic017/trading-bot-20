from typing import List, Any, NoReturn

from sqlalchemy.exc import OperationalError

from src import db
from src.dao.dao import DAO
from src.entity.portfolio_entity import PortfolioEntity
from src.entity.stock_entity import StockEntity
from src.enums.mode_enum import ModeEnum
from src.utils.utils import Utils


class PortfolioDAO:

    @staticmethod
    def create(ticker: str, mode: ModeEnum) -> NoReturn:
        portfolio: PortfolioEntity = PortfolioEntity()
        Utils.set_attributes(portfolio, ticker=ticker, mode=mode)
        DAO.persist(portfolio)

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

    @staticmethod
    def update(ticker: str, mode: ModeEnum) -> NoReturn:
        portfolio = PortfolioDAO.read_filter_by_ticker(ticker)
        if portfolio is None:
            PortfolioDAO.create(ticker, mode)
        else:
            portfolio.mode = mode
            DAO.commit()

    @staticmethod
    def delete(ticker: str) -> NoReturn:
        PortfolioEntity.query.filter(PortfolioEntity.ticker == ticker).delete()
        DAO.commit()
