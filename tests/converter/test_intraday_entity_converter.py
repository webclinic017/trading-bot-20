from datetime import datetime
from decimal import Decimal
from re import UNICODE, sub
from unittest.mock import MagicMock

from pandas import date_range
from pytz import utc

from tests.base_test_case import BaseTestCase
from trading_bot import db, Utils
from trading_bot.converter.intraday_entity_converter import IntradayEntityConverter
from trading_bot.dao.base_dao import BaseDAO
from trading_bot.dao.intraday_dao import IntradayDAO
from trading_bot.entity.intraday_entity import IntradayEntity
from trading_bot.entity.stock_entity import StockEntity


class IntradayEntityConverterCase(BaseTestCase):
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
            "symbol":"AAA",
            "volume":"5"
            },{
            "close":"9",
            "date":"2011-11-03 00:00:00+00:00",
            "high":"7",
            "low":"8",
            "open":"6",
            "symbol":"BBB",
            "volume":"0"
            }]
            '''
        request = MagicMock()
        request.files.__getitem__.side_effect = {'file': file}.__getitem__
        IntradayEntityConverter.from_file(request)
        rows = IntradayDAO.read_order_by_date_asc()
        self.assertEqual(len(rows), 2)
        self.assert_attributes(rows[1], date=utc.localize(self.YOUNG_DATE.replace(tzinfo=None)), open=1, high=2, low=3,
                               close=4, volume=5, symbol='AAA')
        self.assert_attributes(rows[0], date=utc.localize(self.OLD_DATE.replace(tzinfo=None)), open=6, high=7, low=8,
                               close=9, volume=0, symbol='BBB')

    def test_to_file(self):
        self.persist_intraday('AAA', self.YOUNG_DATE, 1, 2, 3, 4, 5)
        self.persist_intraday('BBB', self.OLD_DATE, 6, 7, 8, 9, 0)
        content = IntradayEntityConverter.to_file()
        self.assertEqual(len(content), 2)
        self.assert_items(content[0], date='2011-11-04 04:00:00+00:00', open='1.0', high='2.0',
                          low='3.0', close='4.0', volume='5.0', symbol='AAA')
        self.assert_items(content[1], date='2011-11-03 04:00:00+00:00', open='6.0', high='7.0',
                          low='8.0', close='9.0', volume='0.0', symbol='BBB')

    def test_to_dataframe(self):
        intraday_list = self.create_intraday_list()
        frame = IntradayEntityConverter.to_dataframe(intraday_list)
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                self.assertIsInstance(frame.iloc[i][j], float)
                self.assertEqual(frame.iloc[i][j], i)
        self.assertListEqual(list(frame.index), date_range(end='2020-02-02', periods=10).to_pydatetime().tolist())

    def test_to_float_dataframe(self):
        intraday_list = self.create_intraday_list()
        frame = IntradayEntityConverter.to_float_dataframe(intraday_list)
        dates = date_range(end='2020-02-02', periods=10).to_pydatetime().tolist()
        for i in range(frame.shape[0]):
            self.assertIsInstance(frame.iloc[i][0], datetime)
            self.assertEqual(frame.iloc[i][0], dates[i])
            self.assertIsInstance(frame.iloc[i][6], str)
            self.assertEqual(frame.iloc[i][6], 'AAA')
            for j in range(1, frame.shape[1] - 1):
                self.assertIsInstance(frame.iloc[i][j], float)
                self.assertEqual(frame.iloc[i][j], float(i))

    def test_to_html(self):
        stock_entity = StockEntity()
        Utils.set_attributes(stock_entity, symbol='AAA', isin='isin')
        BaseDAO.persist(stock_entity)
        intraday_entity = IntradayEntity()
        Utils.set_attributes(intraday_entity, date=self.YOUNG_DATE, open=Decimal('1'), high=Decimal('2'),
                             low=Decimal('3'), close=Decimal('4'), volume=Decimal('5'), symbol='AAA')
        BaseDAO.persist(stock_entity)
        html = IntradayEntityConverter.to_html()
        self.assertEqual(sub(r"\s+", "", html, flags=UNICODE), '<tableborder="1"class="dataframedata">'
                                                               '<thead><trstyle="text-align:right;">'
                                                               '<th></th></tr></thead><tbody></tbody></table>')
