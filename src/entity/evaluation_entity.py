from src import db


class EvaluationEntity(db.Model):
    __tablename__ = 'evaluation'
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), primary_key=True)
    sum = db.Column(db.Float)
    funds = db.Column(db.Text)
    amountbuy = db.Column(db.Integer)
    distancebuy = db.Column(db.Integer)
    deltabuy = db.Column(db.Float)
    amountsell = db.Column(db.Integer)
    distancesell = db.Column(db.Integer)
    deltasell = db.Column(db.Float)
