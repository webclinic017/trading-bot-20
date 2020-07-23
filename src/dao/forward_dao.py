from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import func

from src import db
from src.dao.dao import DAO
from src.entity.forward_entity import ForwardEntity
from src.enums.action_enum import ActionEnum
from src.utils.utils import Utils


class ForwardDAO:
    @staticmethod
    def create_buy(ticker: str, price: Decimal, number: Decimal, cash: Decimal) -> None:
        forward: ForwardEntity = ForwardDAO.__init(ActionEnum.BUY, ticker, price, number, cash)
        DAO.persist(forward)

    @staticmethod
    def create_sell(ticker: str, price: Decimal, number: Decimal, cash: Decimal) -> None:
        forward: ForwardEntity = ForwardDAO.__init(ActionEnum.SELL, ticker, price, number, cash)
        DAO.persist(forward)

    @staticmethod
    def read() -> List[ForwardEntity]:
        return ForwardEntity.query.order_by(ForwardEntity.timestamp.asc()).all()

    @staticmethod
    def read_all() -> List[ForwardEntity]:
        return ForwardEntity.query.all()

    @staticmethod
    def read_latest_date() -> datetime:
        return Utils.first(db.session.query(func.max(ForwardEntity.timestamp)).first())

    @staticmethod
    def __init(action: ActionEnum, ticker: str, price: Decimal, number: Decimal, cash: Decimal) -> ForwardEntity:
        forward: ForwardEntity = ForwardEntity()
        Utils.set_attributes(forward, timestamp=Utils.now(), ticker=ticker, action=action, price=price, number=number,
                             cash=cash)
        return forward
