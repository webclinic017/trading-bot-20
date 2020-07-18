import unittest
from unittest.mock import patch

from src import db
from src.bo.optimizer_bo import OptimizerBO
from src.dao.evaluation_dao import EvaluationDAO
from src.dto.attempt_dto import AttemptDTO
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
        Utils.assert_attributes(evaluation, sum=185266.8, funds='185266.8', amount_buy=1000, amount_sell=1000,
                                delta_buy=1.5, delta_sell=1.5, distance_buy=30, distance_sell=30)

    @patch('src.utils.utils.Utils.negation')
    @patch('src.utils.utils.Utils.inverse')
    def test_start(self, negation, inverse):
        negation.return_value = 1
        inverse.return_value = 1
        EvaluationDAO.create(10000, 'second', AttemptDTO(1000, 10, 1.5, 1000, 10, 1.5))
        Utils.persist_intraday_frame()
        OptimizerBO.start(['AAA', 'BBB', 'CCC'], 3, 1)
        evaluation = EvaluationDAO.read_order_by_sum()
        self.assertIsInstance(evaluation, EvaluationEntity)
        Utils.assert_attributes(evaluation, sum=235112.5, funds='235112.5', amount_buy=2000, amount_sell=2000,
                                delta_buy=3.0, delta_sell=3.0, distance_buy=20, distance_sell=20)


if __name__ == '__main__':
    unittest.main()
