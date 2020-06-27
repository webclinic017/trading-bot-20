from src import db


class ForwardEntity(db.Model):
    __tablename__ = 'forward'
    date = db.Column(db.DateTime, index=True, primary_key=True)
    ticker = db.Column(db.String(10), db.ForeignKey('stock.ticker'), primary_key=True)
    action = db.Column(db.String(10))
    price = db.Column(db.Float)
    number = db.Column(db.Integer)
    cash = db.Column(db.Float)
