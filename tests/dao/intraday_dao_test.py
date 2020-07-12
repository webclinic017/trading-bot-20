import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd
import pytz

from src import db
from src.constants import US_EASTERN, UTC
from src.dao.intraday_dao import IntradayDAO
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
            self.assertEqual(intraday.date, pytz.utc.localize(datetime.fromisoformat(row['date'])))
            self.assertEqual(intraday.open, float(row['1. open']))
            self.assertEqual(intraday.high, float(row['2. high']))
            self.assertEqual(intraday.low, float(row['3. low']))
            self.assertEqual(intraday.close, float(row['4. close']))
            self.assertEqual(intraday.volume, float(row['5. volume']))
            self.assertEqual(intraday.ticker, 'IBM')

    def test_localize(self):
        eastern_date = datetime.fromisoformat('2011-11-04T00:00:00')
        utc_date = eastern_date + timedelta(hours=4)
        eastern = pytz.timezone(US_EASTERN).localize(eastern_date)
        utc = pytz.utc.localize(utc_date)
        self.assertEqual(utc, eastern.astimezone(pytz.utc))

    @patch('alpha_vantage.timeseries.TimeSeries.get_intraday')
    def test_create_ticker(self, intraday):
        intraday.return_value = Utils.get_intraday()
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayDAO.create_ticker('AAA')
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 10)
        date = pytz.utc.localize(datetime.fromisoformat('2000-01-01T05:00:00'))
        Utils.assert_attributes(rows[0], date=date, open=500, high=500, low=500, close=500, volume=500, ticker='AAA')


if __name__ == '__main__':
    unittest.main()
