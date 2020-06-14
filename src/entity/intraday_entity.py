from src import db


class IntradayEntity(db.Model):
    __tablename__ = 'intraday'
    date = db.Column(db.String(31), primary_key=True)
    open = db.Column(db.String(31))
    high = db.Column(db.String(31))
    low = db.Column(db.String(31))
    close = db.Column(db.String(31))
    volume = db.Column(db.String(31))
    ticker = db.Column(db.String(31), primary_key=True)
