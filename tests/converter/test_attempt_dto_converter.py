import unittest

from src.converter.attempt_dto_converter import AttemptDTOConverter
from src.dto.attempt_dto import AttemptDTO
from src.entity.evaluation_entity import EvaluationEntity
from src.utils.utils import Utils as Utilities
from tests.utils.utils import Utils


class AttemptDTOConverterTestCase(unittest.TestCase):
    def test_from_evaluation(self):
        evaluation = EvaluationEntity()
        Utilities.set_attributes(evaluation, amount_buy=2, distance_buy=3, delta_buy=4, amount_sell=5, distance_sell=6,
                                 delta_sell=7)
        attempt = AttemptDTOConverter.from_evaluation(evaluation)
        self.assertIsInstance(attempt, AttemptDTO)
        Utils.assert_attributes(attempt, amount_buy=2, distance_buy=3, delta_buy=4, amount_sell=5, distance_sell=6,
                                delta_sell=7)


if __name__ == '__main__':
    unittest.main()
