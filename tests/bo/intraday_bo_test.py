import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytz

from src import db
from src.bo.intraday_bo import IntradayBO
from src.constants import US_EASTERN
from src.dao.intraday_dao import IntradayDAO
from src.dao.stock_dao import StockDAO
from tests.utils.utils import Utils


class IntradayBOTestCase(unittest.TestCase):
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()

    def test_from_file(self):
        file = MagicMock()
        file.read.return_value = '''
            [{
            "close":"4",
            "date":"2011-11-04 00:00:00+00:00",
            "high":"2",
            "low":"3",
            "open":"1",
            "ticker":"AAA",
            "volume":"5"
            },{
            "close":"9",
            "date":"2011-11-03 00:00:00+00:00",
            "high":"7",
            "low":"8",
            "open":"6",
            "ticker":"BBB",
            "volume":"0"
            }]
            '''
        request = MagicMock()
        request.files.__getitem__.side_effect = {'file': file}.__getitem__
        IntradayBO.from_file(request)
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 2)
        Utils.assert_attributes(rows[1], date=IntradayBOTestCase.YOUNG_DATE, open=1, high=2, low=3, close=4, volume=5,
                                ticker='AAA')
        Utils.assert_attributes(rows[0], date=IntradayBOTestCase.OLD_DATE, open=6, high=7, low=8, close=9, volume=0,
                                ticker='BBB')

    def test_to_file(self):
        Utils.create_intraday('AAA', IntradayBOTestCase.YOUNG_DATE, 1, 2, 3, 4, 5)
        Utils.create_intraday('BBB', IntradayBOTestCase.OLD_DATE, 6, 7, 8, 9, 0)
        content = IntradayBO.to_file()
        self.assertEqual(len(content), 2)
        Utils.assert_items(content[1], date=IntradayBOTestCase.YOUNG_DATE, open=1, high=2, low=3, close=4, volume=5,
                           ticker='AAA')
        Utils.assert_items(content[0], date=IntradayBOTestCase.OLD_DATE, open=6, high=7, low=8, close=9, volume=0,
                           ticker='BBB')

    @patch('alpha_vantage.timeseries.TimeSeries.get_intraday')
    @patch('src.bo.stock_bo.StockBO.isin')
    def test_update(self, isin, intraday):
        isin.return_value = 'isin'
        intraday.return_value = Utils.get_intraday()
        StockDAO.create_if_not_exists(('AAA',))
        Utils.create_intraday('AAA', IntradayBOTestCase.OLD_DATE, 500, 500, 500, 500, 500)
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayBO.update('AAA', 'BBB')
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 11)
        dates = pd.date_range('1/1/2000', periods=10)
        for i in range(len(rows) - 1):
            date = pytz.timezone(US_EASTERN).localize(pd.to_datetime(dates[i], format='%d%b%Y:%H:%M:%S.%f'))
            Utils.assert_attributes(rows[i], date=date, open=500, high=500, low=500, close=500, volume=500,
                                    ticker='BBB')
        Utils.assert_attributes(rows[10], date=IntradayBOTestCase.OLD_DATE, open=500, high=500, low=500, close=500,
                                volume=500, ticker='AAA')

    @patch('alpha_vantage.timeseries.TimeSeries.get_intraday')
    @patch('src.bo.stock_bo.StockBO.isin')
    def test_update_all_available(self, isin, intraday):
        isin.return_value = 'isin'
        intraday.return_value = Utils.get_intraday()
        StockDAO.create_if_not_exists(('AAA',))
        Utils.create_intraday('AAA', IntradayBOTestCase.YOUNG_DATE, 500, 500, 500, 500, 500)
        StockDAO.create_if_not_exists(('BBB',))
        Utils.create_intraday('BBB', IntradayBOTestCase.OLD_DATE, 500, 500, 500, 500, 500)
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayBO.update('AAA', 'BBB')
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 12)
        dates = pd.date_range('1/1/2000', periods=10)
        for i in range(len(rows) - 2):
            date = pytz.timezone(US_EASTERN).localize(pd.to_datetime(dates[i], format='%d%b%Y:%H:%M:%S.%f'))
            Utils.assert_attributes(rows[i], date=date, open=500, high=500, low=500, close=500, volume=500,
                                    ticker='BBB')
        Utils.assert_attributes(rows[10], date=IntradayBOTestCase.OLD_DATE, open=500, high=500, low=500, close=500,
                                volume=500, ticker='BBB')
        Utils.assert_attributes(rows[11], date=IntradayBOTestCase.YOUNG_DATE, open=500, high=500, low=500, close=500,
                                volume=500, ticker='AAA')


if __name__ == '__main__':
    unittest.main()
