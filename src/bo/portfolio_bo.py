import hashlib
from typing import List, Any, NoReturn, Tuple, Union

from yahoo_fin.stock_info import tickers_sp500, tickers_nasdaq

from src.dao.portfolio_dao import PortfolioDAO
from src.dao.stock_dao import StockDAO
from src.entity.portfolio_entity import PortfolioEntity
from src.enums.mode_enum import ModeEnum


class PortfolioBO:

    @classmethod
    def backward_portfolio(cls, size: int = 100) -> List[str]:
        return cls.__sort(PortfolioDAO.read_filter_by_mode(ModeEnum.BACKWARD), size)

    @classmethod
    def forward_portfolio(cls, size: int = 100) -> List[str]:
        return cls.__sort(PortfolioDAO.read_filter_by_mode(ModeEnum.FORWARD), size)

    @classmethod
    def backward_forward_portfolio(cls, size: int = 100) -> List[str]:
        return cls.forward_portfolio(size) + cls.backward_portfolio(size)

    @staticmethod
    def __sort(portfolio: List[PortfolioEntity], size: int) -> List[str]:
        return sorted(list(map(lambda p: p.ticker, portfolio)),
                      key=lambda x: hashlib.md5(x.encode()).hexdigest())[:size]

    @classmethod
    def init(cls) -> NoReturn:
        ticker_list: Tuple[Union[str, None], ...] = tickers_sp500() + tickers_nasdaq()
        StockDAO.update(ticker_list)
        for ticker in ticker_list:
            PortfolioDAO.create(ticker, ModeEnum.BACKWARD)
            PortfolioDAO.create(ticker, ModeEnum.FORWARD)

    @staticmethod
    def read() -> List[Any]:
        return PortfolioDAO.read()

    @staticmethod
    def read_filter_by_ticker_isin(ticker: str) -> Any:
        return PortfolioDAO.read_filter_by_ticker_isin(ticker)

    @staticmethod
    def update(ticker: str, mode: ModeEnum) -> NoReturn:
        StockDAO.create_if_not_exists((ticker,))
        PortfolioDAO.update(ticker, mode)

    @staticmethod
    def delete(ticker: str) -> NoReturn:
        PortfolioDAO.delete(ticker)
