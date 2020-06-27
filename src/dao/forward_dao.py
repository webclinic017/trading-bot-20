import datetime
from typing import List

from src.action import Action
from src.dao.broker_dao import BrokerDAO
from src.dao.dao import DAO
from src.entity.forward_entity import ForwardEntity


class ForwardDAO(BrokerDAO):
    @staticmethod
    def create_buy(ticker: str, price: float, number: int, cash: float) -> None:
        forward: ForwardEntity = ForwardDAO.init(Action.BUY, ticker, price, number, cash)
        DAO.persist(forward)

    @staticmethod
    def create_sell(ticker: str, price: float, number: int, cash: float) -> None:
        forward: ForwardEntity = ForwardDAO.init(Action.SELL, ticker, price, number, cash)
        DAO.persist(forward)

    @staticmethod
    def read() -> List[ForwardEntity]:
        return ForwardEntity.query.order_by(ForwardEntity.date.asc()).all()

    @staticmethod
    def read_all() -> List[ForwardEntity]:
        return ForwardEntity.query.all()

    @staticmethod
    def init(action: Action, ticker: str, price: float, number: int, cash: float) -> ForwardEntity:
        forward: ForwardEntity = ForwardEntity()
        forward.date = datetime.datetime.now()
        forward.ticker = ticker
        forward.action = action
        forward.price = price
        forward.number = number
        forward.cash = cash
        return forward
