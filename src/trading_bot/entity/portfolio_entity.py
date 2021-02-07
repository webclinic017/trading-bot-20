from trading_bot import db
from trading_bot.entity.stock_entity import StockEntity
from trading_bot.enums.mode_enum import ModeEnum


class PortfolioEntity(db.Model):
    __tablename__ = 'portfolio'
    symbol = db.Column(db.String(10), db.ForeignKey(StockEntity.symbol), nullable=False, index=True, primary_key=True)
    mode = db.Column(db.Enum(ModeEnum), primary_key=True)
