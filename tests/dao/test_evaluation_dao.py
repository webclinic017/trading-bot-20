import unittest
from datetime import datetime
from unittest.mock import patch

import pytz

from src import db
from src.dao.evaluation_dao import EvaluationDAO
from src.dto.attempt_dto import AttemptDTO
from src.entity.evaluation_entity import EvaluationEntity
from tests.utils.utils import Utils


class EvaluationDAOTestCase(unittest.TestCase):
    YOUNG_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-04T00:00:00'))
    OLD_DATE = pytz.utc.localize(datetime.fromisoformat('2011-11-03T00:00:00'))

    @classmethod
    def setUpClass(cls):
        db.create_all()

    @patch('src.utils.utils.Utils.now')
    def setUp(self, now):
        Utils.truncate_tables()
        self.attempt = AttemptDTO(1, 2, 3, 4, 5, 6)
        now.return_value = EvaluationDAOTestCase.YOUNG_DATE
        EvaluationDAO.create(1000, 'first', self.attempt)
        now.return_value = EvaluationDAOTestCase.OLD_DATE
        EvaluationDAO.create(2000, 'second', AttemptDTO(11, 22, 33, 44, 55, 66))

    def test_read_all(self):
        rows = EvaluationDAO.read_all()
        self.assertEqual(len(rows), 2)

    def test_read_order_by_sum(self):
        evaluation = EvaluationDAO.read_order_by_sum()
        self.assertIsInstance(evaluation, EvaluationEntity)
        Utils.assert_attributes(evaluation, timestamp=EvaluationDAOTestCase.OLD_DATE, sum=2000, funds='second',
                                amount_buy=11, distance_buy=22, delta_buy=33, amount_sell=44, distance_sell=55,
                                delta_sell=66)

    def test_read_attempt(self):
        evaluation = EvaluationDAO.read_attempt(self.attempt)
        self.assertIsInstance(evaluation, EvaluationEntity)
        Utils.assert_attributes(evaluation, timestamp=EvaluationDAOTestCase.YOUNG_DATE, sum=1000, funds='first',
                                amount_buy=1, distance_buy=2, delta_buy=3, amount_sell=4, distance_sell=5, delta_sell=6)


if __name__ == '__main__':
    unittest.main()
