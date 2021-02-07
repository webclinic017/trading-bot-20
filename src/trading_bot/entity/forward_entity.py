from sqlalchemy_utc import UtcDateTime

from trading_bot import db
from trading_bot.entity.stock_entity import StockEntity
from trading_bot.enums.action_enum import ActionEnum
from trading_bot.enums.strategy_enum import StrategyEnum


class ForwardEntity(db.Model):
    __tablename__ = 'forward'
    timestamp = db.Column(UtcDateTime, nullable=False, index=True, primary_key=True)
    symbol = db.Column(db.String(10), db.ForeignKey(StockEntity.symbol), nullable=False, primary_key=True)
    action = db.Column(db.Enum(ActionEnum))
    price = db.Column(db.DECIMAL)
    number = db.Column(db.DECIMAL)
    cash = db.Column(db.DECIMAL)
    strategy = db.Column(db.Enum(StrategyEnum), nullable=False, primary_key=True)
