import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch

import pandas as pd
import pytz

from src import db
from src.constants import US_EASTERN, UTC
from src.dao.dao import DAO
from src.dao.intraday_dao import IntradayDAO
from src.entity.intraday_entity import IntradayEntity
from src.utils.utils import Utils as Utilities
from tests.utils.utils import Utils


class IntradayDAOTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()

    def test_init(self):
        data = {'date': ['2020-05-01 16:00:00', '2020-05-01 15:55:00'],
                '1. open': ['121.4000', '121.6703'],
                '2. high': ['121.8700', '121.8200'],
                '3. low': ['121.4000', '121.3900'],
                '4. close': ['121.8300', '121.3900'],
                '5. volume': ['219717', '119646']
                }
        frame = pd.DataFrame(data)
        for index, row in frame.iterrows():
            intraday = IntradayDAO.init(row, 'IBM', UTC)
            self.assertIsInstance(intraday, IntradayEntity)
            Utils.assert_attributes(intraday, date=pytz.utc.localize(datetime.fromisoformat(row['date'])),
                                    open=Decimal(row['1. open']), high=Decimal(row['2. high']),
                                    low=Decimal(row['3. low']), close=Decimal(row['4. close']),
                                    volume=Decimal(row['5. volume']), ticker='IBM')

    def test_localize(self):
        date = datetime.fromisoformat('2011-11-04T00:00:00')
        eastern = pytz.timezone(US_EASTERN).localize(date)
        intraday = IntradayEntity()
        Utilities.set_attributes(intraday, date=eastern, open=Decimal('1'), high=Decimal('1'), low=Decimal('1'),
                                 close=Decimal('1'), volume=1, ticker='AAA')
        DAO.persist(intraday)
        intraday = IntradayDAO.read_filter_by_ticker_first('AAA')
        self.__assert_date(eastern, intraday, date)

    def test_eastern_utc(self):
        date = datetime.fromisoformat('2011-11-04T00:00:00')
        Utils.persist_intraday('AAA', date, Decimal('1'), Decimal('1'), Decimal('1'), Decimal('1'), Decimal('1'))
        intraday = IntradayDAO.read_filter_by_ticker_first('AAA')
        eastern = pytz.timezone(US_EASTERN).localize(date)
        self.__assert_date(eastern, intraday, date)

    def __assert_date(self, eastern, intraday, date):
        utc = eastern.astimezone(pytz.utc)
        self.assertEqual(intraday.date, pytz.utc.localize(date + timedelta(hours=4)))
        self.assertEqual(intraday.date, utc)
        self.assertEqual(intraday.date.astimezone(pytz.timezone(US_EASTERN)), eastern)

    @patch('alpha_vantage.timeseries.TimeSeries.get_intraday')
    def test_create_ticker(self, intraday):
        intraday.return_value = Utils.get_intraday()
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayDAO.create_ticker('AAA')
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 10)
        date = pytz.utc.localize(datetime.fromisoformat('2000-01-01T05:00:00'))
        Utils.assert_attributes(rows[0], date=date, open=Decimal('500'), high=Decimal('500'), low=Decimal('500'),
                                close=Decimal('500'), volume=Decimal('500'), ticker='AAA')

    def test_dataframe(self):
        young_date = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
        old_date = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))
        dates = (young_date, old_date, young_date)
        tickers = ('AAA', 'AAA', 'BBB')
        intradays = []
        for date, ticker in zip(dates, tickers):
            intraday = IntradayEntity()
            Utilities.set_attributes(intraday, date=date, close=Decimal(1), ticker=ticker)
            intradays.append(intraday)
        frame = IntradayDAO.dataframe(intradays)
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                self.assertIsInstance(frame.iloc[i][j], Decimal)


if __name__ == '__main__':
    unittest.main()
