import math
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from src import db
from src.dao.evaluation_dao import EvaluationDAO
from src.entity.evaluation_entity import EvaluationEntity
from src.optimizer import Optimizer


class OptimizerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        EvaluationEntity.query.delete()

    @patch('src.utils.Utils.negation')
    @patch('src.utils.Utils.inverse')
    def test_optimise(self, negation, inverse):
        negation.return_value = 0
        inverse.return_value = 0
        rows = EvaluationDAO.read_all()
        self.assertEqual(len(rows), 0)
        Optimizer.optimise([OptimizerTestCase.__create_frame()])
        evaluation = EvaluationDAO.read_order_by_sum()
        self.assertEqual(evaluation.sum, 45789.399999999965)
        self.assertEqual(evaluation.funds, '45789.399999999965')
        self.assertEqual(evaluation.amountbuy, 1000)
        self.assertEqual(evaluation.amountsell, 1000)
        self.assertEqual(evaluation.deltabuy, 1.5)
        self.assertEqual(evaluation.deltasell, 1.5)
        self.assertEqual(evaluation.distancebuy, 30)
        self.assertEqual(evaluation.distancesell, 30)

    @staticmethod
    def __create_frame():
        dates = pd.date_range('1/1/2000', periods=150)
        prices_aaa = prices_bbb = np.full((150, 1), float(500))
        prices_aaa[30:60] = prices_aaa[90:120] = float(100)
        prices_bbb[0:30] = math.nan
        tickers = ['AAA', 'BBB']
        prices = np.hstack((prices_aaa, prices_bbb))
        frame = pd.DataFrame(prices, index=dates, columns=tickers)
        frame.sort_index(inplace=True, ascending=True)
        return frame


if __name__ == '__main__':
    unittest.main()
