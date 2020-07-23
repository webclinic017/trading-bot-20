import unittest
from decimal import Decimal

from src.dto.attempt_dto import AttemptDTO
from tests.utils.utils import Utils


class AttemptDTOTestCase(unittest.TestCase):
    def test_init(self):
        attempt = AttemptDTO()
        self.assertIsInstance(attempt, AttemptDTO)
        Utils.assert_attributes(attempt, amount_buy=1000, distance_buy=30, delta_buy=1.5, amount_sell=1000,
                                distance_sell=30, delta_sell=1.5)

    def test_init_with_arguments(self):
        attempt = AttemptDTO(Decimal('1'), Decimal('2'), Decimal('3'), Decimal('4'), Decimal('5'), Decimal('6'))
        self.assertIsInstance(attempt, AttemptDTO)
        Utils.assert_attributes(attempt, amount_buy=Decimal('1'), distance_buy=Decimal('2'), delta_buy=Decimal('3'),
                                amount_sell=Decimal('4'), distance_sell=Decimal('5'), delta_sell=Decimal('6'))


if __name__ == '__main__':
    unittest.main()
