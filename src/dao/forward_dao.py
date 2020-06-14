import datetime

from src.constants import SELL, BUY
from src.dao.dao import DAO
from src.entity.forward_entity import ForwardEntity


class ForwardDAO:
    @staticmethod
    def create_buy(ticker, price, number, cash):
        forward = ForwardDAO.init(BUY, ticker, price, number, cash)
        DAO.persist(forward)

    @staticmethod
    def create_sell(ticker, price, number, cash):
        forward = ForwardDAO.init(SELL, ticker, price, number, cash)
        DAO.persist(forward)

    @staticmethod
    def read():
        return ForwardEntity.query.order_by(ForwardEntity.date.asc()).all()

    @staticmethod
    def read_all():
        return ForwardEntity.query.all()

    @staticmethod
    def init(action, ticker, price, number, cash):
        forward = ForwardEntity()
        forward.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        forward.ticker = ticker
        forward.action = action
        forward.price = str(price)
        forward.number = str(number)
        forward.cash = str(cash)
        return forward
