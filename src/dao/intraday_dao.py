import json
import logging
import os
import time
from datetime import datetime
from typing import List, Tuple

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from pandas import DataFrame, Series
from sqlalchemy import func
from werkzeug.datastructures import FileStorage

from src import db
from src.dao.dao import DAO
from src.dao.stock_dao import StockDAO
from src.entity.intraday_entity import IntradayEntity
from src.entity.stock_entity import StockEntity
from src.portfolio import Portfolio


class IntradayDAO:
    @staticmethod
    def create_portfolio(*portfolio: str) -> None:
        for ticker in portfolio:
            time.sleep(20)
            IntradayDAO.create_ticker(ticker)

    @staticmethod
    def create_ticker(*ticker: str) -> None:
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
    def create_from_file(file: FileStorage) -> None:
        rows = json.loads(file.read())
        for row in rows:
            intraday: IntradayEntity = IntradayEntity()
            intraday.date = datetime.fromisoformat(row['date'])
            intraday.open = float(row['open'])
            intraday.high = float(row['high'])
            intraday.low = float(row['low'])
            intraday.close = float(row['close'])
            intraday.volume = float(row['volume'])
            intraday.ticker = row['ticker']
            DAO.persist(intraday)

    @staticmethod
    def read(*portfolio: str) -> List[IntradayEntity]:
        return IntradayEntity.query.filter(IntradayEntity.ticker.in_(portfolio)).order_by(
            IntradayEntity.date.asc()).all()

    @staticmethod
    def read_order_by_date_asc() -> List[IntradayEntity]:
        return IntradayEntity.query.order_by(IntradayEntity.date.asc()).all()

    @staticmethod
    def read_filter_by_ticker(ticker: str) -> List[IntradayEntity]:
        return IntradayEntity.query.filter_by(ticker=ticker).order_by(IntradayEntity.date.desc()).all()

    @staticmethod
    def read_filter_by_ticker_first(ticker: str) -> IntradayEntity:
        return IntradayEntity.query.filter_by(ticker=ticker).order_by(IntradayEntity.date.desc()).first()

    @staticmethod
    def read_latest_date() -> List[IntradayEntity]:
        return db.session.query(func.max(IntradayEntity.date), IntradayEntity.ticker).group_by(
            IntradayEntity.ticker).all()

    @staticmethod
    def dataframe_ticker() -> DataFrame:
        rows: List[StockEntity] = StockDAO.read_ticker()
        tickers: List[str] = list(map(lambda r: r.ticker, rows))
        return IntradayDAO.dataframe_portfolio(*tickers)

    @staticmethod
    def dataframe_portfolio(*portfolio: str) -> DataFrame:
        rows: List[IntradayEntity] = IntradayDAO.read(*portfolio)
        return IntradayDAO.dataframe(rows)

    @staticmethod
    def dataframe_group(*group: Tuple[Tuple[str]]) -> List[DataFrame]:
        return list(map(lambda g: IntradayDAO.dataframe_portfolio(*g), group[0]))

    @staticmethod
    def dataframe(rows: List[IntradayEntity]) -> DataFrame:
        frame: DataFrame = pd.DataFrame()
        for row in rows:
            frame.at[row.date, row.ticker] = float(row.close)
        return frame

    @staticmethod
    def init(row: Series, ticker: str) -> IntradayEntity:
        intraday: IntradayEntity = IntradayEntity()
        intraday.date = datetime.fromisoformat(str(row['date']))
        intraday.open = float(row['1. open'])
        intraday.high = float(row['2. high'])
        intraday.low = float(row['3. low'])
        intraday.close = float(row['4. close'])
        intraday.volume = float(row['5. volume'])
        intraday.ticker = ticker
        return intraday

    @staticmethod
    def update(*portfolio: str) -> None:
        StockDAO.create_if_not_exists(portfolio)
        rows: List[IntradayEntity] = IntradayEntity.query.with_entities(IntradayEntity.ticker).filter(
            IntradayEntity.ticker.in_(portfolio)).distinct(IntradayEntity.ticker).all()
        if len(rows) < len(portfolio):
            tickers: List[str] = list(map(lambda r: r.ticker, rows))
            differences: List[str] = list(set(portfolio) - set(tickers))
            if differences is not None and len(differences) > 0:
                IntradayDAO.create_ticker(differences[0])
        else:
            rows: List[IntradayEntity] = db.session.query(IntradayEntity.ticker, db.func.max(
                IntradayEntity.date)).group_by(IntradayEntity.ticker).all()
            if rows is not None:
                latest_date: str = max(list(map(lambda r: r[1], rows)))
                tickers: List[str] = list(map(lambda r: r.ticker, list(filter(lambda f: (f[1] != latest_date), rows))))
                if tickers is not None and len(tickers) > 0:
                    IntradayDAO.create_ticker(tickers[0])


if __name__ == '__main__':
    IntradayDAO.update(*Portfolio.test_prod_portfolio())
