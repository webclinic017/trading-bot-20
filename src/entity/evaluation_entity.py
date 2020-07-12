from sqlalchemy_utc import UtcDateTime

from src import db


class EvaluationEntity(db.Model):
    __tablename__ = 'evaluation'
    timestamp = db.Column(UtcDateTime, primary_key=True)
    sum = db.Column(db.Float, index=True)
    funds = db.Column(db.Text)
    amountbuy = db.Column(db.Integer)
    distancebuy = db.Column(db.Integer)
    deltabuy = db.Column(db.Float)
    amountsell = db.Column(db.Integer)
    distancesell = db.Column(db.Integer)
    deltasell = db.Column(db.Float)
