import unittest
from decimal import Decimal

from src.bo.inventory_bo import InventoryBO


class InventoryBOTestCase(unittest.TestCase):
    def test_init(self):
        inventory = InventoryBO(Decimal('1'), Decimal('2'))
        self.assertEqual(inventory.number, Decimal('1'))
        self.assertEqual(inventory.price, Decimal('2'))

    def test_value(self):
        inventory = InventoryBO(Decimal('3'), Decimal('5'))
        self.assertEqual(inventory.value(), Decimal('15'))


if __name__ == '__main__':
    unittest.main()
