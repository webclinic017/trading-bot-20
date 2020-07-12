import math
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd
import pytz

from src.utils.utils import Utils


class UtilsTestCase(unittest.TestCase):
    def test_valid(self):
        valid = Utils.valid(1, 2, 3)
        self.assertEqual(valid, True)
        valid = Utils.valid(3, 2, 3)
        self.assertEqual(valid, False)
        valid = Utils.valid(1, 2, 1)
        self.assertEqual(valid, False)

    def test_negation(self):
        negation = Utils.negation()
        self.assertGreaterEqual(negation, -1)
        self.assertLessEqual(negation, 1)

    def test_inverse(self):
        inverse = Utils.inverse()
        self.assertGreaterEqual(inverse, 0)
        self.assertLessEqual(inverse, math.inf)

    def test_group(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        group = Utils.group(3, iterable)
        self.assertTupleEqual(group, ((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        group = Utils.group(2, iterable)
        self.assertTupleEqual(group, ((1, 2), (3, 4), (5, 6), (7, 8)))

    def test_number(self):
        number = Utils.number(6.3, 2.4)
        self.assertEqual(number, 2)
        number = Utils.number(9.2, 2.9)
        self.assertEqual(number, 3)
        number = Utils.number(0, 0)
        self.assertEqual(number, 0)

    def test_day_delta_value(self):
        dates = pd.date_range('1/1/2000', periods=15, freq='8h')
        tickers = ['AAA', 'BBB']
        frame = pd.DataFrame(index=dates, columns=tickers)
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                frame.iloc[i][j] = i + j
        frame.sort_index(inplace=True, ascending=True)
        date = frame.index.max()
        value_aaa = Utils.day_delta_value(frame, 'AAA', date, 1)
        value_bbb = Utils.day_delta_value(frame, 'BBB', date, 1)
        self.assertEqual(value_aaa, 11)
        self.assertEqual(value_bbb, 12)
        value_aaa = Utils.day_delta_value(frame, 'AAA', date, 2)
        value_bbb = Utils.day_delta_value(frame, 'BBB', date, 2)
        self.assertEqual(value_aaa, 8)
        self.assertEqual(value_bbb, 9)
        value_aaa = Utils.day_delta_value(frame, 'AAA', date, 3)
        value_bbb = Utils.day_delta_value(frame, 'BBB', date, 3)
        self.assertEqual(value_aaa, 5)
        self.assertEqual(value_bbb, 6)
        value_aaa = Utils.day_delta_value(frame, 'AAA', date, 10)
        value_bbb = Utils.day_delta_value(frame, 'BBB', date, 10)
        self.assertTrue(math.isnan(value_aaa))
        self.assertTrue(math.isnan(value_bbb))

    @patch('src.utils.utils.Utils.now')
    def test_is_today(self, now):
        today = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
        now.return_value = today
        self.assertTrue(Utils.is_today(today))
        self.assertTrue(Utils.is_today(today + timedelta(microseconds=23)))
        self.assertTrue(Utils.is_today(today + timedelta(milliseconds=23)))
        self.assertTrue(Utils.is_today(today + timedelta(seconds=23)))
        self.assertTrue(Utils.is_today(today + timedelta(minutes=23)))
        self.assertTrue(Utils.is_today(today + timedelta(hours=23)))
        self.assertFalse(Utils.is_today(today + timedelta(hours=24)))
        self.assertFalse(Utils.is_today(today + timedelta(days=1)))
        self.assertFalse(Utils.is_today(today + timedelta(weeks=52)))
        self.assertFalse(Utils.is_today(None))

    @patch('src.utils.utils.Utils.now')
    def test_is_working_day_ny(self, now):
        now.return_value = pytz.utc.localize(datetime.fromisoformat('2019-07-05T12:00:00'))
        self.assertTrue(Utils.is_working_day_ny())
        now.return_value = pytz.utc.localize(datetime.fromisoformat('2019-07-06T12:00:00'))
        self.assertFalse(Utils.is_working_day_ny())
        now.return_value = pytz.utc.localize(datetime.fromisoformat('2019-07-04T12:00:00'))
        self.assertFalse(Utils.is_working_day_ny())

    def test_first(self):
        self.assertIsNone(Utils.first([]))
        self.assertEqual(Utils.first([1]), 1)
        self.assertEqual(Utils.first([1, 2]), 1)


if __name__ == '__main__':
    unittest.main()