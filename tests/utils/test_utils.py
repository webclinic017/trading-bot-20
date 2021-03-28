import math
import os
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch, ANY

import pytz
from numpy import std, mean

from tests.base_test_case import BaseTestCase
from trading_bot import Utils
from trading_bot.common.constants import ZERO
from trading_bot.converter.intraday_entity_converter import IntradayEntityConverter
from trading_bot.dto.attempt_dto import AttemptDTO


class UtilsTestCase(BaseTestCase):

    def test_valid(self):
        valid = Utils.valid(Decimal('1'), Decimal('2'), Decimal('3'))
        self.assertEqual(valid, True)
        valid = Utils.valid(Decimal('3'), Decimal('2'), Decimal('3'))
        self.assertEqual(valid, False)
        valid = Utils.valid(Decimal('1'), Decimal('2'), Decimal('1'))
        self.assertEqual(valid, False)

    def test_negation(self):
        negation = Utils.negation()
        self.assertIsInstance(negation, Decimal)
        self.assertGreaterEqual(negation, Decimal('-1'))
        self.assertLessEqual(negation, Decimal('1'))

    def test_inverse(self):
        inverse = Utils.inverse()
        self.assertIsInstance(inverse, Decimal)
        self.assertGreaterEqual(inverse, ZERO)
        self.assertLessEqual(inverse, math.inf)

    def test_group(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        group = Utils.group(3, iterable)
        self.assertTupleEqual(group, ((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        group = Utils.group(2, iterable)
        self.assertTupleEqual(group, ((1, 2), (3, 4), (5, 6), (7, 8)))

    def test_number(self):
        number = Utils.number(Decimal('6.3'), Decimal('2.4'))
        self.assertEqual(number, Decimal('2'))
        number = Utils.number(Decimal('9.2'), Decimal('2.9'))
        self.assertEqual(number, Decimal('3'))
        number = Utils.number(ZERO, ZERO)
        self.assertEqual(number, ZERO)

    @patch('trading_bot.utils.utils.Utils.now')
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

    @patch('trading_bot.utils.utils.Utils.now')
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

    def test_assert_attributes(self):
        attempt = AttemptDTO()
        Utils.set_attributes(attempt, amount_buy=Decimal('1'), distance_buy=Decimal('2'), delta_buy=Decimal('3'),
                             amount_sell=Decimal('4'), distance_sell=Decimal('5'), delta_sell=Decimal('6'))
        self.assertIsInstance(attempt, AttemptDTO)
        self.assert_attributes(attempt, amount_buy=Decimal('1'), distance_buy=Decimal('2'), delta_buy=Decimal('3'),
                               amount_sell=Decimal('4'), distance_sell=Decimal('5'), delta_sell=Decimal('6'))

    def test_truncate(self):
        self.assertEqual(Utils.truncate(Decimal('0.5')), ZERO)
        self.assertEqual(Utils.truncate(Decimal('-0.5')), ZERO)
        self.assertEqual(Utils.truncate(Decimal('1.2')), Decimal('1'))
        self.assertEqual(Utils.truncate(Decimal('-1.2')), Decimal('-1'))
        self.assertEqual(Utils.truncate(Decimal('1.9')), Decimal('1'))
        self.assertEqual(Utils.truncate(Decimal('-1.9')), Decimal('-1'))
        self.assertEqual(Utils.truncate(Decimal('10')), Decimal('10'))
        self.assertEqual(Utils.truncate(Decimal('-10')), Decimal('-10'))

    def test_is_test(self):
        self.assertTrue(Utils.is_test())

    @patch.dict(os.environ, {'FROM_EMAIL_ADDRESS': 'from_address', 'TO_EMAIL_ADDRESS': 'to_address',
                             'EMAIL_PASSWORD': 'password', 'SMTP_HOST': 'host', 'SMTP_PORT': '587'})
    @patch('smtplib.SMTP.sendmail')
    @patch('smtplib.SMTP.login')
    @patch('smtplib.SMTP.starttls')
    def test_send_mail(self, starttls, login, sendmail):
        with patch('smtplib.SMTP.__init__', return_value=None):
            Utils.send_mail('test')
        login.assert_called_with('from_address', 'password')
        sendmail.assert_called_with('from_address', 'to_address', ANY)
        self.assertEqual(sendmail.call_count, 1)
        self.assertEqual(login.call_count, 1)
        self.assertEqual(starttls.call_count, 1)

    def test_normalize(self):
        intraday_list = self.create_intraday_list(decimal_list=[i for i in range(10)])
        self.__assert_dataframe(intraday_list)

    def test_normalize_divide_zero(self):
        intraday_list = self.create_intraday_list(decimal_list=[0 for _ in range(10)])
        self.__assert_dataframe(intraday_list)

    def __assert_dataframe(self, intraday_list):
        expected = IntradayEntityConverter.to_dataframe(intraday_list)
        actual = Utils.normalize(expected)
        standard = std(expected.values)
        average = mean(expected.values)
        self.assertEqual(actual.shape[0], 10)
        for i in range(actual.shape[0]):
            for j in range(actual.shape[1]):
                self.assertEqual(actual.columns[j], expected.columns[j])
                self.assertEqual(actual.index.values[i], expected.index.values[i])
                normalized = (expected.iloc[i][j] - average) / standard
                self.assertIsInstance(actual.iloc[i][j], float)
                if not math.isnan(normalized):
                    self.assertEqual(actual.iloc[i][j], normalized)
