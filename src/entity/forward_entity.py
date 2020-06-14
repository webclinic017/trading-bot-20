from src import db


class ForwardEntity(db.Model):
    __tablename__ = 'forward'
    date = db.Column(db.String(31), primary_key=True)
    ticker = db.Column(db.String(31), primary_key=True)
    action = db.Column(db.String(31))
    price = db.Column(db.String(31))
    number = db.Column(db.String(31))
    cash = db.Column(db.String(31))
