import copy
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from numpy import full, hstack
from pandas import DataFrame, date_range
from pytz import timezone

from src.common.constants import UTC, US_EASTERN, NAN
from src.dao.base_dao import BaseDAO
from src.dao.intraday_dao import IntradayDAO
from src.entity.configuration_entity import ConfigurationEntity
from src.entity.evaluation_entity import EvaluationEntity
from src.entity.forward_entity import ForwardEntity
from src.entity.intraday_entity import IntradayEntity
from src.entity.portfolio_entity import PortfolioEntity
from src.entity.stock_entity import StockEntity


class BaseTestCase(TestCase):

    @staticmethod
    def create_table_frame() -> DataFrame:
        dates = date_range('1/1/2000', periods=150, tz=UTC)
        prices_aaa = full((150, 1), Decimal(500))
        prices_bbb = copy.copy(prices_aaa)
        prices_ccc = copy.copy(prices_aaa)
        prices_aaa[30:60] = prices_aaa[90:120] = prices_ccc[0:30] = prices_ccc[60:90] = prices_ccc[120:150] = Decimal(
            100)
        prices_bbb[0:30] = NAN
        tickers = ['AAA', 'BBB', 'CCC']
        prices = hstack((prices_aaa, prices_bbb, prices_ccc))
        frame = DataFrame(prices, index=dates, columns=tickers)
        frame.sort_index(inplace=True, ascending=True)
        return frame

    def assert_attributes(self, assertable, **kwargs):
        for key, value in kwargs.items():
            self.assertEqual(getattr(assertable, key), value)

    def assert_items(self, assertable, **kwargs):
        for key, value in kwargs.items():
            self.assertEqual(value, assertable[key])

    @classmethod
    def persist_intraday(cls, ticker, date, o, high, low, close, volume):
        cls.__persist_get_intraday(date.replace(tzinfo=None), full((1, 5), [o, high, low, close, volume]), ticker)

    @classmethod
    def persist_intraday_frame(cls):
        table_aaa = full((150, 5), Decimal(500))
        table_ccc = copy.copy(table_aaa)
        table_aaa[30:60] = table_aaa[90:120] = table_ccc[0:30] = table_ccc[60:90] = table_ccc[120:150] = Decimal(100)
        data = {'AAA': {'start': '1/1/2000', 'data': table_aaa},
                'BBB': {'start': '31/1/2000', 'data': full((120, 5), Decimal(500))},
                'CCC': {'start': '1/1/2000', 'data': table_ccc}}
        for key, value in data.items():
            cls.__persist_get_intraday(value['start'], value['data'], key)

    @classmethod
    def __persist_get_intraday(cls, start, data, ticker):
        frame, meta_data = cls.get_intraday(start, data)
        frame = frame.reset_index()
        for index, row in frame.iterrows():
            intraday = IntradayDAO.init(row, ticker, meta_data['6. Time Zone'])
            BaseDAO.persist(intraday)

    @staticmethod
    def get_intraday(start='1/1/2000', data=full((10, 5), Decimal(500))):
        dates = date_range(start, periods=len(data))
        columns = ['1. open', '2. high', '3. low', '4. close', '5. volume']
        frame = DataFrame(data, columns=columns)
        frame['date'] = dates
        frame.sort_index(inplace=True, ascending=False)
        meta_data = {'6. Time Zone': US_EASTERN}
        return frame, meta_data

    @staticmethod
    def get_intraday_csv(ticker: str):
        intraday_list = [('time', 'open', 'high', 'low', 'close', 'volume')]
        decimal_list = full((10,), Decimal(500))
        dates = date_range(end='2020-02-02', periods=10).to_pydatetime().tolist()
        for date, decimal in zip(dates, decimal_list):
            intraday_list.append((date, decimal, decimal, decimal, decimal, decimal, ticker))
        return intraday_list, None

    @staticmethod
    def truncate_tables():
        PortfolioEntity.query.delete()
        EvaluationEntity.query.delete()
        IntradayEntity.query.delete()
        ForwardEntity.query.delete()
        StockEntity.query.delete()
        ConfigurationEntity.query.delete()

    @staticmethod
    def create_datetime(date: str, tz: str = US_EASTERN):
        return timezone(tz).localize(datetime.fromisoformat(date))
