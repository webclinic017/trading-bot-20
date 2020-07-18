from sqlalchemy_utc import UtcDateTime

from src import db


class EvaluationEntity(db.Model):
    __tablename__ = 'evaluation'
    timestamp = db.Column(UtcDateTime, nullable=False, primary_key=True)
    sum = db.Column(db.Float, index=True)
    funds = db.Column(db.Text)
    amount_buy = db.Column('amountbuy', db.Integer)
    distance_buy = db.Column('distancebuy', db.Integer)
    delta_buy = db.Column('deltabuy', db.Float)
    amount_sell = db.Column('amountsell', db.Integer)
    distance_sell = db.Column('distancesell', db.Integer)
    delta_sell = db.Column('deltasell', db.Float)
