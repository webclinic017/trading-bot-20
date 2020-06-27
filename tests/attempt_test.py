import unittest

from src.attempt import Attempt
from src.entity.evaluation_entity import EvaluationEntity


class AttemptTestCase(unittest.TestCase):
    def test_init(self):
        attempt = Attempt()
        self.assertEqual(attempt.amount_buy, 1000)
        self.assertEqual(attempt.distance_buy, 500)
        self.assertEqual(attempt.delta_buy, 1.5)
        self.assertEqual(attempt.amount_sell, 1000)
        self.assertEqual(attempt.distance_sell, 500)
        self.assertEqual(attempt.delta_sell, 1.5)

    def test_init_with_arguments(self):
        attempt = Attempt(1, 2, 3, 4, 5, 6)
        self.assertEqual(attempt.amount_buy, 1)
        self.assertEqual(attempt.distance_buy, 2)
        self.assertEqual(attempt.delta_buy, 3)
        self.assertEqual(attempt.amount_sell, 4)
        self.assertEqual(attempt.distance_sell, 5)
        self.assertEqual(attempt.delta_sell, 6)

    def test_from_evaluation(self):
        evaluation = EvaluationEntity()
        evaluation.amountbuy = 1
        evaluation.distancebuy = 2
        evaluation.deltabuy = 3
        evaluation.amountsell = 4
        evaluation.distancesell = 5
        evaluation.deltasell = 6
        attempt = Attempt.from_evaluation(evaluation)
        self.assertEqual(attempt.amount_buy, evaluation.amountbuy)
        self.assertEqual(attempt.distance_buy, evaluation.distancebuy)
        self.assertEqual(attempt.delta_buy, evaluation.deltabuy)
        self.assertEqual(attempt.amount_sell, evaluation.amountsell)
        self.assertEqual(attempt.distance_sell, evaluation.distancesell)
        self.assertEqual(attempt.delta_sell, evaluation.deltasell)


if __name__ == '__main__':
    unittest.main()
