import copy
import math
from unittest import TestCase

import numpy as np
import pandas as pd
from pandas import DataFrame

from src.constants import UTC
from src.dao.dao import DAO
from src.dao.intraday_dao import IntradayDAO


class Utils:
    @staticmethod
    def create_frame() -> DataFrame:
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
    def create_intraday(ticker, date, o, high, low, close, volume):
        data = [date.replace(tzinfo=None), o, high, low, close, volume]
        index = ['date', '1. open', '2. high', '3. low', '4. close', '5. volume']
        series = pd.Series(data, index=index, dtype=object)
        intraday = IntradayDAO.init(series, ticker, UTC)
        DAO.persist(intraday)
