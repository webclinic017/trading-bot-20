import math
from datetime import datetime, timedelta
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

import pandas as pd
import pytz

from src.constants import ZERO
from src.dto.attempt_dto import AttemptDTO
from src.utils.utils import Utils as Utilities
from tests.utils.utils import Utils


class UtilsTestCase(TestCase):
    def test_valid(self):
        valid = Utilities.valid(Decimal('1'), Decimal('2'), Decimal('3'))
        self.assertEqual(valid, True)
        valid = Utilities.valid(Decimal('3'), Decimal('2'), Decimal('3'))
        self.assertEqual(valid, False)
        valid = Utilities.valid(Decimal('1'), Decimal('2'), Decimal('1'))
        self.assertEqual(valid, False)

    def test_negation(self):
        negation = Utilities.negation()
        self.assertIsInstance(negation, Decimal)
        self.assertGreaterEqual(negation, Decimal('-1'))
        self.assertLessEqual(negation, Decimal('1'))

    def test_inverse(self):
        inverse = Utilities.inverse()
        self.assertIsInstance(inverse, Decimal)
        self.assertGreaterEqual(inverse, ZERO)
        self.assertLessEqual(inverse, math.inf)

    def test_group(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        group = Utilities.group(3, iterable)
        self.assertTupleEqual(group, ((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        group = Utilities.group(2, iterable)
        self.assertTupleEqual(group, ((1, 2), (3, 4), (5, 6), (7, 8)))

    def test_number(self):
        number = Utilities.number(Decimal('6.3'), Decimal('2.4'))
        self.assertEqual(number, Decimal('2'))
        number = Utilities.number(Decimal('9.2'), Decimal('2.9'))
        self.assertEqual(number, Decimal('3'))
        number = Utilities.number(ZERO, ZERO)
        self.assertEqual(number, ZERO)

    def test_day_delta_value(self):
        dates = pd.date_range('1/1/2000', periods=15, freq='8h')
        tickers = ['AAA', 'BBB']
        frame = pd.DataFrame(index=dates, columns=tickers)
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                frame.iloc[i][j] = i + j
        frame.sort_index(inplace=True, ascending=True)
        date = frame.index.max()
        value_aaa = Utilities.day_delta_value(frame, 'AAA', date, Decimal('1'))
        value_bbb = Utilities.day_delta_value(frame, 'BBB', date, Decimal('1'))
        self.assertEqual(value_aaa, Decimal('11'))
        self.assertEqual(value_bbb, Decimal('12'))
        value_aaa = Utilities.day_delta_value(frame, 'AAA', date, Decimal('2'))
        value_bbb = Utilities.day_delta_value(frame, 'BBB', date, Decimal('2'))
        self.assertEqual(value_aaa, Decimal('8'))
        self.assertEqual(value_bbb, Decimal('9'))
        value_aaa = Utilities.day_delta_value(frame, 'AAA', date, Decimal('3'))
        value_bbb = Utilities.day_delta_value(frame, 'BBB', date, Decimal('3'))
        self.assertEqual(value_aaa, Decimal('5'))
        self.assertEqual(value_bbb, Decimal('6'))
        value_aaa = Utilities.day_delta_value(frame, 'AAA', date, Decimal('10'))
        value_bbb = Utilities.day_delta_value(frame, 'BBB', date, Decimal('10'))
        self.assertTrue(math.isnan(value_aaa))
        self.assertTrue(math.isnan(value_bbb))

    @patch('src.utils.utils.Utils.now')
    def test_is_today(self, now):
        today = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
        now.return_value = today
        self.assertTrue(Utilities.is_today(today))
        self.assertTrue(Utilities.is_today(today + timedelta(microseconds=23)))
        self.assertTrue(Utilities.is_today(today + timedelta(milliseconds=23)))
        self.assertTrue(Utilities.is_today(today + timedelta(seconds=23)))
        self.assertTrue(Utilities.is_today(today + timedelta(minutes=23)))
        self.assertTrue(Utilities.is_today(today + timedelta(hours=23)))
        self.assertFalse(Utilities.is_today(today + timedelta(hours=24)))
        self.assertFalse(Utilities.is_today(today + timedelta(days=1)))
        self.assertFalse(Utilities.is_today(today + timedelta(weeks=52)))
        self.assertFalse(Utilities.is_today(None))

    @patch('src.utils.utils.Utils.now')
    def test_is_working_day_ny(self, now):
        now.return_value = pytz.utc.localize(datetime.fromisoformat('2019-07-05T12:00:00'))
        self.assertTrue(Utilities.is_working_day_ny())
        now.return_value = pytz.utc.localize(datetime.fromisoformat('2019-07-06T12:00:00'))
        self.assertFalse(Utilities.is_working_day_ny())
        now.return_value = pytz.utc.localize(datetime.fromisoformat('2019-07-04T12:00:00'))
        self.assertFalse(Utilities.is_working_day_ny())

    def test_first(self):
        self.assertIsNone(Utilities.first([]))
        self.assertEqual(Utilities.first([1]), 1)
        self.assertEqual(Utilities.first([1, 2]), 1)

    def test_assert_attributes(self):
        attempt = AttemptDTO()
        Utilities.set_attributes(attempt, amount_buy=Decimal('1'), distance_buy=Decimal('2'), delta_buy=Decimal('3'),
                                 amount_sell=Decimal('4'), distance_sell=Decimal('5'), delta_sell=Decimal('6'))
        self.assertIsInstance(attempt, AttemptDTO)
        Utils.assert_attributes(attempt, amount_buy=Decimal('1'), distance_buy=Decimal('2'), delta_buy=Decimal('3'),
                                amount_sell=Decimal('4'), distance_sell=Decimal('5'), delta_sell=Decimal('6'))

    def test_truncate(self):
        self.assertEqual(Utilities.truncate(Decimal('0.5')), ZERO)
        self.assertEqual(Utilities.truncate(Decimal('-0.5')), ZERO)
        self.assertEqual(Utilities.truncate(Decimal('1.2')), Decimal('1'))
        self.assertEqual(Utilities.truncate(Decimal('-1.2')), Decimal('-1'))
        self.assertEqual(Utilities.truncate(Decimal('1.9')), Decimal('1'))
        self.assertEqual(Utilities.truncate(Decimal('-1.9')), Decimal('-1'))
        self.assertEqual(Utilities.truncate(Decimal('10')), Decimal('10'))
        self.assertEqual(Utilities.truncate(Decimal('-10')), Decimal('-10'))
