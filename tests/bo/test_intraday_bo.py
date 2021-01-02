from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytz
from pandas import to_datetime, date_range

from src import db
from src.bo.intraday_bo import IntradayBO
from src.constants import US_EASTERN
from src.dao.intraday_dao import IntradayDAO
from src.dao.stock_dao import StockDAO
from tests.utils.utils import Utils


class IntradayBOTestCase(TestCase):
    YOUNG_DATE = Utils.create_datetime('2011-11-04T00:00:00')
    OLD_DATE = Utils.create_datetime('2011-11-03T00:00:00')

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
        Utils.assert_attributes(rows[1], date=pytz.utc.localize(IntradayBOTestCase.YOUNG_DATE.replace(tzinfo=None)),
                                open=1, high=2, low=3, close=4, volume=5, ticker='AAA')
        Utils.assert_attributes(rows[0], date=pytz.utc.localize(IntradayBOTestCase.OLD_DATE.replace(tzinfo=None)),
                                open=6, high=7, low=8, close=9, volume=0, ticker='BBB')

    def test_to_file(self):
        Utils.persist_intraday('AAA', IntradayBOTestCase.YOUNG_DATE, 1, 2, 3, 4, 5)
        Utils.persist_intraday('BBB', IntradayBOTestCase.OLD_DATE, 6, 7, 8, 9, 0)
        content = IntradayBO.to_file()
        self.assertEqual(len(content), 2)
        Utils.assert_items(content[0], date='2011-11-04 04:00:00+00:00', open='1.0', high='2.0',
                           low='3.0', close='4.0', volume='5.0', ticker='AAA')
        Utils.assert_items(content[1], date='2011-11-03 04:00:00+00:00', open='6.0', high='7.0',
                           low='8.0', close='9.0', volume='0.0', ticker='BBB')

    @patch('alpha_vantage.timeseries.TimeSeries.get_intraday')
    @patch('src.bo.stock_bo.StockBO.isin')
    def test_update(self, isin, intraday):
        isin.return_value = 'isin'
        intraday.return_value = Utils.get_intraday()
        StockDAO.create_if_not_exists(('AAA',))
        Utils.persist_intraday('AAA', IntradayBOTestCase.OLD_DATE, 500, 500, 500, 500, 500)
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayBO.update(('AAA', 'BBB',))
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 11)
        dates = date_range('1/1/2000', periods=10)
        for i in range(len(rows) - 1):
            date = pytz.timezone(US_EASTERN).localize(to_datetime(dates[i], format='%d%b%Y:%H:%M:%S.%f'))
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
        Utils.persist_intraday('AAA', Utils.create_datetime('2011-11-04T23:00:00'), 500, 500, 500, 500, 500)
        StockDAO.create_if_not_exists(('BBB',))
        Utils.persist_intraday('BBB', Utils.create_datetime('2011-11-04T22:00:00'), 500, 500, 500, 500, 500)
        StockDAO.create_if_not_exists(('CCC',))
        Utils.persist_intraday('CCC', Utils.create_datetime('2011-11-03T23:00:00'), 500, 500, 500, 500, 500)
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayBO.update(('AAA', 'BBB', 'CCC'))
        intraday.assert_called_with(symbol='CCC', outputsize='full')
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 13)
        dates = date_range('1/1/2000', periods=10)
        for i in range(len(rows) - 3):
            date = pytz.timezone(US_EASTERN).localize(to_datetime(dates[i], format='%d%b%Y:%H:%M:%S.%f'))
            Utils.assert_attributes(rows[i], date=date, open=500, high=500, low=500, close=500, volume=500,
                                    ticker='CCC')
        Utils.assert_attributes(rows[10], date=Utils.create_datetime('2011-11-03T23:00:00'), open=500, high=500,
                                low=500, close=500, volume=500, ticker='CCC')
        Utils.assert_attributes(rows[11], date=Utils.create_datetime('2011-11-04T22:00:00'), open=500, high=500,
                                low=500, close=500, volume=500, ticker='BBB')
        Utils.assert_attributes(rows[12], date=Utils.create_datetime('2011-11-04T23:00:00'), open=500, high=500,
                                low=500, close=500, volume=500, ticker='AAA')
