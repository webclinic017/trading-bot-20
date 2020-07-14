import unittest
from unittest.mock import patch

from src import db
from src.bo.optimizer_bo import OptimizerBO
from src.dao.evaluation_dao import EvaluationDAO
from src.entity.evaluation_entity import EvaluationEntity
from tests.utils.utils import Utils


class OptimizerBOTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()

    @patch('src.utils.utils.Utils.negation')
    @patch('src.utils.utils.Utils.inverse')
    def test_optimise(self, negation, inverse):
        negation.return_value = 0
        inverse.return_value = 0
        rows = EvaluationDAO.read_all()
        self.assertEqual(len(rows), 0)
        OptimizerBO.optimise([Utils.create_table_frame()])
        evaluation = EvaluationDAO.read_order_by_sum()
        Utils.assert_attributes(evaluation, sum=185266.8, funds='185266.8', amountbuy=1000, amountsell=1000,
                                deltabuy=1.5, deltasell=1.5, distancebuy=30, distancesell=30)

    @patch('src.utils.utils.Utils.negation')
    @patch('src.utils.utils.Utils.inverse')
    def test_start(self, negation, inverse):
        negation.return_value = 0
        inverse.return_value = 0
        rows = EvaluationDAO.read_all()
        self.assertEqual(len(rows), 0)
        Utils.persist_intraday_frame()
        OptimizerBO.start(['AAA', 'BBB', 'CCC'], 3, 1)
        evaluation = EvaluationDAO.read_order_by_sum()
        self.assertIsInstance(evaluation, EvaluationEntity)
        Utils.assert_attributes(evaluation, sum=185274.59999999998, funds='185274.59999999998', amountbuy=1000,
                                amountsell=1000, deltabuy=1.5, deltasell=1.5, distancebuy=30, distancesell=30)


if __name__ == '__main__':
    unittest.main()
