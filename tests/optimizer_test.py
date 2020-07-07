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
        Utils.assert_attributes(evaluation, sum=185266.8, funds='185266.8', amountbuy=1000, amountsell=1000,
                                deltabuy=1.5, deltasell=1.5, distancebuy=30, distancesell=30)


if __name__ == '__main__':
    unittest.main()
