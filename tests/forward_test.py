import math
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd

from src import db
from src.action import Action
from src.attempt import Attempt
from src.constants import INITIAL_CASH, FEE
from src.dao.dao import DAO
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dao.intraday_dao import IntradayDAO
from src.entity.evaluation_entity import EvaluationEntity
from src.entity.forward_entity import ForwardEntity
from src.entity.intraday_entity import IntradayEntity
from src.forward import Forward
from src.inventory import Inventory
from tests.utils import Utils


class ForwardTestCase(unittest.TestCase):
    YOUNG_DATE = datetime.fromisoformat('2011-11-04T00:00:00')
    OLD_DATE = datetime.fromisoformat('2011-11-03T00:00:00')

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        EvaluationEntity.query.delete()
        IntradayEntity.query.delete()
        ForwardEntity.query.delete()

    @patch('src.utils.Utils.is_today')
    @patch('src.utils.Utils.is_working_day_ny')
    @patch('src.utils.Utils.now')
    def test_start(self, now, is_working_day_ny, is_today):
        is_today.return_value = False
        is_working_day_ny.return_value = True
        now.return_value = ForwardTestCase.OLD_DATE
        ForwardDAO.create_buy('AAA', 100.0, 10, 8996.1)
        ForwardDAO.create_buy('BBB', 100.0, 10, 7992.200000000001)
        now.return_value = datetime.fromisoformat('2011-11-04T00:00:00')
        EvaluationDAO.create(40000, '', Attempt())
        ForwardTestCase.__to_intraday(Utils.create_frame())
        Forward.start()
        rows = ForwardDAO.read_all()
        self.assertEqual(len(rows), 3)
        Utils.assert_attributes(rows[0], action=Action.BUY, cash=8996.1, date=ForwardTestCase.OLD_DATE, number=10,
                                price=100.0, ticker='AAA')
        Utils.assert_attributes(rows[1], action=Action.BUY, cash=7992.200000000001, date=ForwardTestCase.OLD_DATE,
                                number=10, price=100.0, ticker='BBB')
        Utils.assert_attributes(rows[2], action=Action.SELL, cash=8988.300000000001, date=ForwardTestCase.YOUNG_DATE,
                                number=2, price=500.0, ticker='AAA')

    @patch('src.utils.Utils.now')
    def test_init(self, now):
        prices = (20, 30, 40, 50, 60, 70)
        numbers = (10, 10, 10, 5, 10, 10)
        multipliers = (-1, -1, -1, 1, -1, 1)
        now.return_value = ForwardTestCase.YOUNG_DATE + timedelta(seconds=1)
        ForwardDAO.create_buy('AAA', prices[0], numbers[0], 9000)
        now.return_value = ForwardTestCase.YOUNG_DATE + timedelta(seconds=2)
        ForwardDAO.create_buy('AAA', prices[1], numbers[1], 8000)
        now.return_value = ForwardTestCase.YOUNG_DATE + timedelta(seconds=3)
        ForwardDAO.create_buy('BBB', prices[2], numbers[2], 7000)
        now.return_value = ForwardTestCase.YOUNG_DATE + timedelta(seconds=4)
        ForwardDAO.create_sell('BBB', prices[3], numbers[3], 7500)
        now.return_value = ForwardTestCase.YOUNG_DATE + timedelta(seconds=5)
        ForwardDAO.create_buy('CCC', prices[4], numbers[4], 6500)
        now.return_value = ForwardTestCase.YOUNG_DATE + timedelta(seconds=6)
        ForwardDAO.create_sell('CCC', prices[5], numbers[5], 7500)
        inventory, cash = Forward.init()
        estimated = INITIAL_CASH
        for i in range(len(prices)):
            estimated += prices[i] * numbers[i] * multipliers[i] - FEE
        Utils.assert_attributes(inventory['AAA'], price=30.0, number=20)
        Utils.assert_attributes(inventory['BBB'], price=50.0, number=5)
        Utils.assert_attributes(inventory['CCC'], price=70.0, number=0)
        self.assertEqual(cash, estimated)

    def test_update(self):
        ForwardTestCase.__create_intraday('AAA', ForwardTestCase.YOUNG_DATE, 10, 10, 10, 10, 10)
        ForwardTestCase.__create_intraday('AAA', ForwardTestCase.OLD_DATE, 7, 7, 7, 7, 7)
        ForwardTestCase.__create_intraday('BBB', ForwardTestCase.YOUNG_DATE, 20, 20, 20, 20, 20)
        ForwardTestCase.__create_intraday('BBB', ForwardTestCase.OLD_DATE, 8, 8, 8, 8, 8)
        ForwardTestCase.__create_intraday('CCC', ForwardTestCase.YOUNG_DATE, 30, 30, 30, 30, 30)
        ForwardTestCase.__create_intraday('CCC', ForwardTestCase.OLD_DATE, 9, 9, 9, 9, 9)
        inventory = {
            'AAA': Inventory(70, 1),
            'BBB': Inventory(80, 2),
            'CCC': Inventory(90, 3),
        }
        inventory, total_value, total = Forward.update(inventory, INITIAL_CASH)
        Utils.assert_attributes(inventory['AAA'], price=10, number=70)
        Utils.assert_attributes(inventory['BBB'], price=20, number=80)
        Utils.assert_attributes(inventory['CCC'], price=30, number=90)
        estimated = inventory['AAA'].value() + inventory['BBB'].value() + inventory['CCC'].value()
        self.assertEqual(total, estimated)
        self.assertEqual(total_value, estimated + INITIAL_CASH)

    @staticmethod
    def __to_intraday(frame):
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                ticker = frame.columns[j]
                date = pd.to_datetime(frame.index.values[i], format='%d%b%Y:%H:%M:%S.%f')
                price = frame.iloc[i][j]
                if math.isnan(price):
                    continue
                ForwardTestCase.__create_intraday(ticker, date, price, price, price, price, price)

    @staticmethod
    def __create_intraday(ticker, date, o, high, low, close, volume):
        data = [date, o, high, low, close, volume]
        index = ['date', '1. open', '2. high', '3. low', '4. close', '5. volume']
        series = pd.Series(data, index=index, dtype=object)
        intraday = IntradayDAO.init(series, ticker)
        DAO.persist(intraday)


if __name__ == '__main__':
    unittest.main()
