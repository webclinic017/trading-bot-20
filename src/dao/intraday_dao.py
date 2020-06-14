import json
import logging
import os
import time

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from sqlalchemy import func

from src import db
from src.dao.dao import DAO
from src.dao.stock_dao import StockDAO
from src.entity.intraday_entity import IntradayEntity
from src.portfolio import Portfolio


class IntradayDAO:
    @staticmethod
    def create_portfolio(*portfolio):
        for ticker in portfolio:
            time.sleep(20)
            IntradayDAO.create_ticker(ticker)

    @staticmethod
    def create_ticker(*ticker):
        try:
            ts = TimeSeries(key=os.environ.get('ALPHA_VANTAGE'), output_format='pandas')
            data, meta_data = ts.get_intraday(symbol=ticker[0].replace('.', '-'), outputsize='full')
            data = data.reset_index()
            for index, row in data.iterrows():
                intraday = IntradayDAO.init(row, ticker[0])
                DAO.persist(intraday)
        except ValueError as e:
            logging.exception(e)

    @staticmethod
    def create_from_file(file):
        rows = json.loads(file.read())
        for row in rows:
            intraday = IntradayEntity()
            for key, value in row.items():
                setattr(intraday, key, str(value))
            DAO.persist(intraday)

    @staticmethod
    def read(*portfolio):
        return IntradayEntity.query.filter(IntradayEntity.ticker.in_(portfolio)).order_by(
            IntradayEntity.date.asc()).all()

    @staticmethod
    def read_order_by_date_asc():
        return IntradayEntity.query.order_by(IntradayEntity.date.asc()).all()

    @staticmethod
    def read_filter_by_ticker(ticker):
        return IntradayEntity.query.filter_by(ticker=ticker).order_by(IntradayEntity.date.desc()).all()

    @staticmethod
    def read_filter_by_ticker_first(ticker):
        return IntradayEntity.query.filter_by(ticker=ticker).order_by(IntradayEntity.date.desc()).first()

    @staticmethod
    def read_latest_date():
        return db.session.query(func.max(IntradayEntity.date), IntradayEntity.ticker).group_by(
            IntradayEntity.ticker).all()

    @staticmethod
    def dataframe_ticker():
        rows = StockDAO.read_ticker()
        tickers = list(map(lambda r: r.ticker, rows))
        return IntradayDAO.dataframe_portfolio(*tickers)

    @staticmethod
    def dataframe_portfolio(*portfolio):
        rows = IntradayDAO.read(*portfolio)
        return IntradayDAO.dataframe(rows)

    @staticmethod
    def dataframe_group(*group):
        return list(map(lambda g: IntradayDAO.dataframe_portfolio(*g), group[0]))

    @staticmethod
    def dataframe(rows):
        frame = pd.DataFrame()
        for row in rows:
            frame.at[row.date, row.ticker] = float(row.close)
        return frame

    @staticmethod
    def init(row, ticker):
        intraday = IntradayEntity()
        for key, value in row.items():
            setattr(intraday, key.split()[-1], str(value))
        intraday.ticker = ticker
        return intraday

    @staticmethod
    def update(*portfolio):
        while True:
            StockDAO.create_if_not_exists(portfolio)
            IntradayDAO.create_portfolio(*portfolio)


if __name__ == '__main__':
    IntradayDAO.update(*Portfolio.test_prod_portfolio())
