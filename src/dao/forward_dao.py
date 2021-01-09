from datetime import datetime
from decimal import Decimal
from typing import List, NoReturn

from sqlalchemy import func

from src import db
from src.dao.base_dao import BaseDAO
from src.entity.forward_entity import ForwardEntity
from src.enums.action_enum import ActionEnum
from src.utils.utils import Utils


class ForwardDAO(BaseDAO):

    @classmethod
    def create_buy(cls, ticker: str, price: Decimal, number: Decimal, cash: Decimal) -> NoReturn:
        forward: ForwardEntity = cls.__init(ActionEnum.BUY, ticker, price, number, cash)
        cls.persist(forward)

    @classmethod
    def create_sell(cls, ticker: str, price: Decimal, number: Decimal, cash: Decimal) -> NoReturn:
        forward: ForwardEntity = cls.__init(ActionEnum.SELL, ticker, price, number, cash)
        cls.persist(forward)

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
