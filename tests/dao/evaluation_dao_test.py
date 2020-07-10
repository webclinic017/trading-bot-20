import time
import unittest

from src import db
from src.dao.evaluation_dao import EvaluationDAO
from src.dto.attempt_dto import AttemptDTO
from src.entity.evaluation_entity import EvaluationEntity


class EvaluationDAOTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        EvaluationEntity.query.delete()
        self.attempt = AttemptDTO(1, 2, 3, 4, 5, 6)
        EvaluationDAO.create(1000, 'first', self.attempt)
        time.sleep(1)
        EvaluationDAO.create(2000, 'second', AttemptDTO(11, 22, 33, 44, 55, 66))

    def test_read_all(self):
        rows = EvaluationDAO.read_all()
        self.assertEqual(len(rows), 2)

    def test_read_order_by_sum(self):
        evaluation = EvaluationDAO.read_order_by_sum()
        EvaluationDAOTestCase.__assert(self, evaluation, 2000, 'second', 11, 22, 33, 44, 55, 66)

    def test_read_attempt(self):
        evaluation = EvaluationDAO.read_attempt(self.attempt)
        EvaluationDAOTestCase.__assert(self, evaluation, 1000, 'first', 1, 2, 3, 4, 5, 6)

    def __assert(self, evaluation, *args):
        self.assertEqual(evaluation.sum, args[0])
        self.assertEqual(evaluation.funds, args[1])
        self.assertEqual(evaluation.amountbuy, args[2])
        self.assertEqual(evaluation.distancebuy, args[3])
        self.assertEqual(evaluation.deltabuy, args[4])
        self.assertEqual(evaluation.amountsell, args[5])
        self.assertEqual(evaluation.distancesell, args[6])
        self.assertEqual(evaluation.deltasell, args[7])


if __name__ == '__main__':
    unittest.main()
