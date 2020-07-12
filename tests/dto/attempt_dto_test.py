import unittest

from src.dto.attempt_dto import AttemptDTO
from src.entity.evaluation_entity import EvaluationEntity
from src.utils.utils import Utils as Utilities
from tests.utils.utils import Utils


class AttemptDTOTestCase(unittest.TestCase):
    def test_init(self):
        attempt = AttemptDTO()
        self.assertIsInstance(attempt, AttemptDTO)
        Utils.assert_attributes(attempt, amount_buy=1000, distance_buy=30, delta_buy=1.5, amount_sell=1000,
                                distance_sell=30, delta_sell=1.5)

    def test_init_with_arguments(self):
        attempt = AttemptDTO(1, 2, 3, 4, 5, 6)
        self.assertIsInstance(attempt, AttemptDTO)
        Utils.assert_attributes(attempt, amount_buy=1, distance_buy=2, delta_buy=3, amount_sell=4,
                                distance_sell=5, delta_sell=6)

    def test_from_evaluation(self):
        evaluation = EvaluationEntity()
        Utilities.set_attributes(evaluation, amountbuy=2, distancebuy=3, deltabuy=4, amountsell=5, distancesell=6,
                                 deltasell=7)
        attempt = AttemptDTO.from_evaluation(evaluation)
        self.assertIsInstance(attempt, AttemptDTO)
        Utils.assert_attributes(attempt, amount_buy=2, distance_buy=3, delta_buy=4, amount_sell=5,
                                distance_sell=6, delta_sell=7)


if __name__ == '__main__':
    unittest.main()
