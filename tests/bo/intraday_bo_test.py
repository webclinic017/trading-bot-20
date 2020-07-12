import unittest
from datetime import datetime
from unittest.mock import MagicMock

import pytz

from src import db
from src.bo.intraday_bo import IntradayBO
from src.dao.intraday_dao import IntradayDAO
from src.entity.intraday_entity import IntradayEntity
from tests.utils.utils import Utils


class IntradayBOTestCase(unittest.TestCase):
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        IntradayEntity.query.delete()

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


if __name__ == '__main__':
    unittest.main()
