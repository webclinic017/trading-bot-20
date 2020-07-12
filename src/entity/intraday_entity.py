from sqlalchemy_utc import UtcDateTime

from src import db
from src.entity.stock_entity import StockEntity


class IntradayEntity(db.Model):
    __tablename__ = 'intraday'
    date = db.Column(UtcDateTime, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    ticker = db.Column(db.String(10), db.ForeignKey(StockEntity.ticker), index=True, primary_key=True)
