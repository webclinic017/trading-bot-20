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
        Utils.assert_attributes(evaluation, sum=185266.8, funds='185266.8', amountbuy=1000, amountsell=1000,
                                deltabuy=1.5, deltasell=1.5, distancebuy=30, distancesell=30)

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
        Utils.assert_attributes(evaluation, sum=235112.5, funds='235112.5', amountbuy=2000, amountsell=2000,
                                deltabuy=3.0, deltasell=3.0, distancebuy=20, distancesell=20)


if __name__ == '__main__':
    unittest.main()
