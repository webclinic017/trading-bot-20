import unittest
from decimal import Decimal
from unittest.mock import patch

from src import db
from src.bo.configuration_bo import ConfigurationBO
from src.bo.optimization_bo import OptimizationBO
from src.constants import ZERO
from src.dao.evaluation_dao import EvaluationDAO
from src.dto.attempt_dto import AttemptDTO
from src.entity.evaluation_entity import EvaluationEntity
from tests.utils.utils import Utils


class OptimizationBOTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()
        ConfigurationBO.create()

    @patch('src.utils.utils.Utils.negation')
    @patch('src.utils.utils.Utils.inverse')
    def test_optimise(self, negation, inverse):
        negation.return_value = ZERO
        inverse.return_value = ZERO
        rows = EvaluationDAO.read_all()
        self.assertEqual(len(rows), 0)
        OptimizationBO.optimise([Utils.create_table_frame()])
        evaluation = EvaluationDAO.read_order_by_sum()
        Utils.assert_attributes(evaluation, sum=Decimal('185266.8'), funds='185266.8', amount_buy=Decimal('1000'),
                                amount_sell=Decimal('1000'), delta_buy=Decimal('1.5'), delta_sell=Decimal('1.5'),
                                distance_buy=Decimal('30'), distance_sell=Decimal('30'))

    @patch('src.utils.utils.Utils.negation')
    @patch('src.utils.utils.Utils.inverse')
    def test_start(self, negation, inverse):
        negation.return_value = Decimal('1')
        inverse.return_value = Decimal('1')
        EvaluationDAO.create(Decimal('10000'), 'second', AttemptDTO(Decimal('1000'), Decimal('10'), Decimal('1.5'),
                                                                    Decimal('1000'), Decimal('10'), Decimal('1.5')))
        Utils.persist_intraday_frame()
        OptimizationBO.start(['AAA', 'BBB', 'CCC'], 3, 1)
        evaluation = EvaluationDAO.read_order_by_sum()
        self.assertIsInstance(evaluation, EvaluationEntity)
        Utils.assert_attributes(evaluation, sum=Decimal('235112.5'), funds='235112.5', amount_buy=Decimal('2000'),
                                amount_sell=Decimal('2000'), delta_buy=Decimal('3'), delta_sell=Decimal('3'),
                                distance_buy=Decimal('20'), distance_sell=Decimal('20'))


if __name__ == '__main__':
    unittest.main()
