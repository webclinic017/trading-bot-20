from src import db


class IntradayEntity(db.Model):
    __tablename__ = 'intraday'
    date = db.Column(db.DateTime, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    ticker = db.Column(db.String(10), primary_key=True)
