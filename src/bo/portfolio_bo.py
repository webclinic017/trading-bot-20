import hashlib
from typing import List, Tuple, Any, NoReturn, Final

from yahoo_fin.stock_info import tickers_sp500

from src.dao.portfolio_dao import PortfolioDAO
from src.dao.stock_dao import StockDAO
from src.entity.portfolio_entity import PortfolioEntity
from src.enums.mode_enum import ModeEnum


class PortfolioBO:
    FORWARD_TICKER: Final[Tuple[str]] = ('BABA', 'AMZN', 'MSFT', 'GOOGL')

    @staticmethod
    def backward_portfolio(size: int = 100) -> List[str]:
        return PortfolioBO.__sort(PortfolioDAO.read_filter_by_mode(ModeEnum.BACKWARD), size)

    @staticmethod
    def forward_portfolio(size: int = 100) -> List[str]:
        return PortfolioBO.__sort(PortfolioDAO.read_filter_by_mode(ModeEnum.FORWARD), size)

    @staticmethod
    def backward_forward_portfolio(size: int = 100) -> List[str]:
        return PortfolioBO.forward_portfolio(size) + PortfolioBO.backward_portfolio(size)

    @staticmethod
    def __sort(portfolio: List[PortfolioEntity], size: int) -> List[str]:
        return sorted(list(map(lambda p: p.ticker, portfolio)),
                      key=lambda x: hashlib.md5(x.encode()).hexdigest())[:size]

    @staticmethod
    def init() -> NoReturn:
        StockDAO.update(tickers_sp500())
        StockDAO.update(PortfolioBO.FORWARD_TICKER)
        for ticker in tickers_sp500():
            PortfolioDAO.create(ticker, ModeEnum.BACKWARD)
        for ticker in PortfolioBO.FORWARD_TICKER:
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
