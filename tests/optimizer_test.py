import unittest
from unittest.mock import patch

from src import db
from src.dao.evaluation_dao import EvaluationDAO
from src.entity.evaluation_entity import EvaluationEntity
from src.optimizer import Optimizer
from tests.utils import Utils


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
        Optimizer.optimise([Utils.create_frame()])
        evaluation = EvaluationDAO.read_order_by_sum()
        self.assertEqual(evaluation.sum, 165613.89999999997)
        self.assertEqual(evaluation.funds, '165613.89999999997')
        self.assertEqual(evaluation.amountbuy, 1000)
        self.assertEqual(evaluation.amountsell, 1000)
        self.assertEqual(evaluation.deltabuy, 1.5)
        self.assertEqual(evaluation.deltasell, 1.5)
        self.assertEqual(evaluation.distancebuy, 30)
        self.assertEqual(evaluation.distancesell, 30)


if __name__ == '__main__':
    unittest.main()
