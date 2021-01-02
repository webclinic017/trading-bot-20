import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import List, Tuple, Any, NoReturn

import pandas as pd
import pytz
from alpha_vantage.timeseries import TimeSeries
from pandas import DataFrame, Series
from sqlalchemy import func

from src import db
from src.constants import NAN
from src.dao.dao import DAO
from src.dao.stock_dao import StockDAO
from src.entity.intraday_entity import IntradayEntity
from src.entity.stock_entity import StockEntity
from src.utils.utils import Utils


class IntradayDAO:
    @staticmethod
    def create_ticker(ticker: str) -> NoReturn:
        try:
            time_series = TimeSeries(output_format='pandas')
            frame, meta_data = time_series.get_intraday(symbol=ticker.replace('.', '-'), outputsize='full')
            frame = frame.reset_index()
            for index, row in frame.iterrows():
                intraday = IntradayDAO.init(row, ticker, meta_data['6. Time Zone'])
                DAO.persist(intraday)
        except ValueError as e:
            logging.exception(e)

    @staticmethod
    def create_from_file(content: str) -> NoReturn:
        rows = json.loads(content)
        for row in rows:
            intraday: IntradayEntity = IntradayEntity()
            Utils.set_attributes(intraday, date=datetime.fromisoformat(row['date']), open=Decimal(row['open']),
                                 high=Decimal(row['high']), low=Decimal(row['low']), close=Decimal(row['close']),
                                 volume=Decimal(row['volume']), ticker=row['ticker'])
            DAO.persist(intraday)

    @staticmethod
    def read(portfolio: List[str]) -> List[IntradayEntity]:
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
    def read_latest_date() -> List[List[Any]]:
        return db.session.query(func.max(IntradayEntity.date), IntradayEntity.ticker).group_by(
            IntradayEntity.ticker).all()

    @staticmethod
    def dataframe_ticker() -> DataFrame:
        rows: List[StockEntity] = StockDAO.read_ticker()
        tickers: List[str] = list(map(lambda r: r.ticker, rows))
        return IntradayDAO.dataframe_portfolio(tickers)

    @staticmethod
    def dataframe_portfolio(portfolio: List[str]) -> DataFrame:
        rows: List[IntradayEntity] = IntradayDAO.read(portfolio)
        return IntradayDAO.dataframe(rows)

    @staticmethod
    def dataframe_group(group: Tuple[Tuple[str]]) -> List[DataFrame]:
        return list(map(lambda g: IntradayDAO.dataframe_portfolio(g), group))

    @staticmethod
    def dataframe(rows: List[IntradayEntity]) -> DataFrame:
        frame: DataFrame = pd.DataFrame()
        for row in rows:
            frame.at[row.date, row.ticker] = Decimal(row.close)
        return frame.fillna(NAN)

    @staticmethod
    def init(row: Series, ticker: str, timezone: str) -> IntradayEntity:
        intraday: IntradayEntity = IntradayEntity()
        Utils.set_attributes(intraday, date=pytz.timezone(timezone).localize(datetime.fromisoformat(str(row['date']))),
                             open=Decimal(row['1. open']), high=Decimal(row['2. high']), low=Decimal(row['3. low']),
                             close=Decimal(row['4. close']), volume=Decimal(row['5. volume']), ticker=ticker)
        return intraday


if __name__ == '__main__':
    IntradayDAO.create_ticker('aapl')
