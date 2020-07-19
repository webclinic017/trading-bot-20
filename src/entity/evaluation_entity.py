from sqlalchemy_utc import UtcDateTime

from src import db


class EvaluationEntity(db.Model):
    __tablename__ = 'evaluation'
    timestamp = db.Column(UtcDateTime, nullable=False, primary_key=True)
    sum = db.Column(db.Float, index=True)
    funds = db.Column(db.Text)
    amount_buy = db.Column(db.Integer)
    distance_buy = db.Column(db.Integer)
    delta_buy = db.Column(db.Float)
    amount_sell = db.Column(db.Integer)
    distance_sell = db.Column(db.Integer)
    delta_sell = db.Column(db.Float)
