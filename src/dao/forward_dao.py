import datetime
from typing import List

from src.constants import SELL, BUY
from src.dao.dao import DAO
from src.entity.forward_entity import ForwardEntity


class ForwardDAO:
    @staticmethod
    def create_buy(ticker: str, price: float, number: int, cash: float) -> None:
        forward: ForwardEntity = ForwardDAO.init(BUY, ticker, price, number, cash)
        DAO.persist(forward)

    @staticmethod
    def create_sell(ticker: str, price: float, number: int, cash: float) -> None:
        forward: ForwardEntity = ForwardDAO.init(SELL, ticker, price, number, cash)
        DAO.persist(forward)

    @staticmethod
    def read() -> List[ForwardEntity]:
        return ForwardEntity.query.order_by(ForwardEntity.date.asc()).all()

    @staticmethod
    def read_all() -> List[ForwardEntity]:
        return ForwardEntity.query.all()

    @staticmethod
    def init(action: str, ticker: str, price: float, number: int, cash: float) -> ForwardEntity:
        forward: ForwardEntity = ForwardEntity()
        forward.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        forward.ticker = ticker
        forward.action = action
        forward.price = str(price)
        forward.number = str(number)
        forward.cash = str(cash)
        return forward
