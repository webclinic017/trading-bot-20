import unittest

from src.bo.inventory_bo import InventoryBO


class InventoryBOTestCase(unittest.TestCase):
    def test_init(self):
        inventory = InventoryBO(1, 2)
        self.assertEqual(inventory.number, 1)
        self.assertEqual(inventory.price, 2)

    def test_value(self):
        inventory = InventoryBO(3, 5)
        self.assertEqual(inventory.value(), 15)


if __name__ == '__main__':
    unittest.main()
