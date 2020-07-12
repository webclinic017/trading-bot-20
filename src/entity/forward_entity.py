from sqlalchemy_utc import UtcDateTime

from src import db
from src.entity.stock_entity import StockEntity
from src.enums.action_enum import ActionEnum


class ForwardEntity(db.Model):
    __tablename__ = 'forward'
    timestamp = db.Column(UtcDateTime, nullable=False, index=True, primary_key=True)
    ticker = db.Column(db.String(10), db.ForeignKey(StockEntity.ticker), nullable=False, primary_key=True)
    action = db.Column(db.Enum(ActionEnum))
    price = db.Column(db.Float)
    number = db.Column(db.Integer)
    cash = db.Column(db.Float)
