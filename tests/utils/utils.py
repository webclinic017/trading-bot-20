import copy
import math
from unittest import TestCase

import numpy as np
import pandas as pd
from pandas import DataFrame

from src.constants import UTC, US_EASTERN
from src.dao.dao import DAO
from src.dao.intraday_dao import IntradayDAO
from src.entity.configuration_entity import ConfigurationEntity
from src.entity.evaluation_entity import EvaluationEntity
from src.entity.forward_entity import ForwardEntity
from src.entity.intraday_entity import IntradayEntity
from src.entity.stock_entity import StockEntity


class Utils:
    @staticmethod
    def create_table_frame() -> DataFrame:
        dates = pd.date_range('1/1/2000', periods=150, tz=UTC)
        prices_aaa = np.full((150, 1), float(500))
        prices_bbb = copy.copy(prices_aaa)
        prices_ccc = copy.copy(prices_aaa)
        prices_aaa[30:60] = prices_aaa[90:120] = prices_ccc[0:30] = prices_ccc[60:90] = prices_ccc[120:150] = float(100)
        prices_bbb[0:30] = math.nan
        tickers = ['AAA', 'BBB', 'CCC']
        prices = np.hstack((prices_aaa, prices_bbb, prices_ccc))
        frame = DataFrame(prices, index=dates, columns=tickers)
        frame.sort_index(inplace=True, ascending=True)
        return frame

    @staticmethod
    def assert_attributes(assertable, **kwargs):
        for key, value in kwargs.items():
            TestCase().assertEqual(getattr(assertable, key), value)

    @staticmethod
    def assert_items(assertable, **kwargs):
        for key, value in kwargs.items():
            TestCase().assertEqual(assertable[key], value)

    @staticmethod
    def persist_intraday(ticker, date, o, high, low, close, volume):
        Utils.__persist_get_intraday(date.replace(tzinfo=None), np.full((1, 5), [o, high, low, close, volume]), ticker)

    @staticmethod
    def persist_intraday_frame():
        table_aaa = np.full((150, 5), float(500))
        table_ccc = copy.copy(table_aaa)
        table_aaa[30:60] = table_aaa[90:120] = table_ccc[0:30] = table_ccc[60:90] = table_ccc[120:150] = float(100)
        data = {'AAA': {'start': '1/1/2000', 'data': table_aaa},
                'BBB': {'start': '31/1/2000', 'data': np.full((120, 5), float(500))},
                'CCC': {'start': '1/1/2000', 'data': table_ccc}}
        for key, value in data.items():
            Utils.__persist_get_intraday(value['start'], value['data'], key)

    @staticmethod
    def __persist_get_intraday(start, data, ticker):
        frame, meta_data = Utils.get_intraday(start, data)
        frame = frame.reset_index()
        for index, row in frame.iterrows():
            intraday = IntradayDAO.init(row, ticker, meta_data['6. Time Zone'])
            DAO.persist(intraday)

    @staticmethod
    def get_intraday(start='1/1/2000', data=np.full((10, 5), float(500))):
        dates = pd.date_range(start, periods=len(data))
        columns = ['1. open', '2. high', '3. low', '4. close', '5. volume']
        frame = DataFrame(data, columns=columns)
        frame['date'] = dates
        frame.sort_index(inplace=True, ascending=False)
        meta_data = {'6. Time Zone': US_EASTERN}
        return frame, meta_data

    @staticmethod
    def truncate_tables():
        EvaluationEntity.query.delete()
        IntradayEntity.query.delete()
        ForwardEntity.query.delete()
        StockEntity.query.delete()
        ConfigurationEntity.query.delete()
