import json
import logging
import os
from datetime import datetime
from typing import List, Tuple

import pandas as pd
import pytz
from alpha_vantage.timeseries import TimeSeries
from pandas import DataFrame, Series
from sqlalchemy import func

from src import db
from src.dao.dao import DAO
from src.dao.stock_dao import StockDAO
from src.entity.intraday_entity import IntradayEntity
from src.entity.stock_entity import StockEntity


class IntradayDAO:
    @staticmethod
    def create_ticker(*ticker: str) -> None:
        try:
            time_series = TimeSeries(key=os.environ.get('ALPHA_VANTAGE'), output_format='pandas')
            data, meta_data = time_series.get_intraday(symbol=ticker[0].replace('.', '-'), outputsize='full')
            data = data.reset_index()
            for index, row in data.iterrows():
                intraday = IntradayDAO.init(row, ticker[0], meta_data['6. Time Zone'])
                DAO.persist(intraday)
        except ValueError as e:
            logging.exception(e)

    @staticmethod
    def create_from_file(content: str) -> None:
        rows = json.loads(content)
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
    def init(row: Series, ticker: str, timezone: str) -> IntradayEntity:
        intraday: IntradayEntity = IntradayEntity()
        intraday.date = pytz.timezone(timezone).localize(datetime.fromisoformat(str(row['date'])))
        intraday.open = float(row['1. open'])
        intraday.high = float(row['2. high'])
        intraday.low = float(row['3. low'])
        intraday.close = float(row['4. close'])
        intraday.volume = float(row['5. volume'])
        intraday.ticker = ticker
        return intraday


if __name__ == '__main__':
    IntradayDAO.create_ticker('aapl')
