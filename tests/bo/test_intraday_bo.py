from datetime import datetime
from unittest.mock import MagicMock, patch

from pandas import to_datetime, date_range
from pytz import timezone, utc

from src import db
from src.bo.intraday_bo import IntradayBO
from src.common.constants import US_EASTERN
from src.dao.intraday_dao import IntradayDAO
from src.dao.stock_dao import StockDAO
from tests.base_test_case import BaseTestCase


class IntradayBOTestCase(BaseTestCase):
    YOUNG_DATE = BaseTestCase.create_datetime('2011-11-04T00:00:00')
    OLD_DATE = BaseTestCase.create_datetime('2011-11-03T00:00:00')

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()

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
        self.assert_attributes(rows[1], date=utc.localize(self.YOUNG_DATE.replace(tzinfo=None)), open=1, high=2, low=3,
                               close=4, volume=5, ticker='AAA')
        self.assert_attributes(rows[0], date=utc.localize(self.OLD_DATE.replace(tzinfo=None)), open=6, high=7, low=8,
                               close=9, volume=0, ticker='BBB')

    def test_to_file(self):
        self.persist_intraday('AAA', self.YOUNG_DATE, 1, 2, 3, 4, 5)
        self.persist_intraday('BBB', self.OLD_DATE, 6, 7, 8, 9, 0)
        content = IntradayBO.to_file()
        self.assertEqual(len(content), 2)
        self.assert_items(content[0], date='2011-11-04 04:00:00+00:00', open='1.0', high='2.0',
                          low='3.0', close='4.0', volume='5.0', ticker='AAA')
        self.assert_items(content[1], date='2011-11-03 04:00:00+00:00', open='6.0', high='7.0',
                          low='8.0', close='9.0', volume='0.0', ticker='BBB')

    @patch('alpha_vantage.timeseries.TimeSeries.get_intraday_extended')
    @patch('src.bo.stock_bo.StockBO.isin')
    def test_update(self, isin, intraday):
        isin.return_value = 'isin'
        intraday.return_value = self.get_intraday_csv('BBB')
        StockDAO.create_if_not_exists(('AAA',))
        date = datetime.fromisoformat('2020-02-03')
        self.persist_intraday('AAA', date, 500, 500, 500, 500, 500)
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayBO.update(('AAA', 'BBB',))
        self.assertEqual(intraday.call_count, 24)
        self.assertEqual(isin.call_count, 3)
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 11)
        dates = date_range(end='2020-02-02', periods=10).to_pydatetime().tolist()
        for i in range(len(rows) - 1):
            self.assert_attributes(rows[i], date=timezone(US_EASTERN).localize(dates[i]),
                                   open=500, high=500, low=500, close=500, volume=500, ticker='BBB')
        self.assert_attributes(rows[10], date=timezone(US_EASTERN).localize(date),
                               open=500, high=500, low=500, close=500, volume=500, ticker='AAA')

    @patch('alpha_vantage.timeseries.TimeSeries.get_intraday')
    @patch('src.bo.stock_bo.StockBO.isin')
    def test_update_all_available(self, isin, intraday):
        isin.return_value = 'isin'
        intraday.return_value = self.get_intraday()
        StockDAO.create_if_not_exists(('AAA',))
        self.persist_intraday('AAA', self.create_datetime('2011-11-04T23:00:00'), 500, 500, 500, 500, 500)
        StockDAO.create_if_not_exists(('BBB',))
        self.persist_intraday('BBB', self.create_datetime('2011-11-04T22:00:00'), 500, 500, 500, 500, 500)
        StockDAO.create_if_not_exists(('CCC',))
        self.persist_intraday('CCC', self.create_datetime('2011-11-03T23:00:00'), 500, 500, 500, 500, 500)
        with patch('alpha_vantage.timeseries.TimeSeries.__init__', return_value=None):
            IntradayBO.update(('AAA', 'BBB', 'CCC'))
        intraday.assert_called_with(symbol='CCC', outputsize='full')
        self.assertEqual(intraday.call_count, 24)
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 13)
        dates = date_range('1/1/2000', periods=10)
        for i in range(len(rows) - 3):
            date = timezone(US_EASTERN).localize(to_datetime(dates[i], format='%d%b%Y:%H:%M:%S.%f'))
            self.assert_attributes(rows[i], date=date, open=500, high=500, low=500, close=500, volume=500,
                                   ticker='CCC')
        self.assert_attributes(rows[10], date=self.create_datetime('2011-11-03T23:00:00'), open=500, high=500,
                               low=500, close=500, volume=500, ticker='CCC')
        self.assert_attributes(rows[11], date=self.create_datetime('2011-11-04T22:00:00'), open=500, high=500,
                               low=500, close=500, volume=500, ticker='BBB')
        self.assert_attributes(rows[12], date=self.create_datetime('2011-11-04T23:00:00'), open=500, high=500,
                               low=500, close=500, volume=500, ticker='AAA')
