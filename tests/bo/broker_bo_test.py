import unittest

from src.bo.broker_bo import BrokerBO
from src.bo.inventory_bo import Inventory


class BrokerBOTestCase(unittest.TestCase):
    def test_update(self):
        broker = BrokerBO()
        broker.update('AAA', 0.1)
        self.assertEqual(broker.inventory['AAA'].price, 0.1)
        broker.update('BBB', 0.2)
        self.assertEqual(broker.inventory['AAA'].price, 0.1)
        self.assertEqual(broker.inventory['BBB'].price, 0.2)
        broker.update('AAA', 0.3)
        self.assertEqual(broker.inventory['AAA'].price, 0.3)
        self.assertEqual(broker.inventory['BBB'].price, 0.2)
        broker.update('BBB', 0.4)
        self.assertEqual(broker.inventory['AAA'].price, 0.3)
        self.assertEqual(broker.inventory['BBB'].price, 0.4)

    def test_buy(self):
        broker = BrokerBO(cash=10000, fee=3.9)
        buy = broker.buy('AAA', 0.1, 10)
        self.assertEqual(buy, True)
        self.assertEqual(broker.inventory['AAA'].price, 0.1)
        self.assertEqual(broker.inventory['AAA'].number, 10)
        self.assertEqual(broker.cash, 10000 - 1 - 3.9)
        buy = broker.buy('AAA', 0.2, 10)
        self.assertEqual(buy, True)
        self.assertEqual(broker.inventory['AAA'].price, 0.2)
        self.assertEqual(broker.inventory['AAA'].number, 20)
        self.assertEqual(broker.cash, 10000 - 1 - 3.9 - 2 - 3.9)

    def test_buy_insufficient_funds(self):
        broker = BrokerBO(cash=10)
        buy = broker.buy('AAA', 10, 10)
        self.assertEqual(buy, False)

    def test_sell(self):
        broker = BrokerBO(cash=10000, fee=3.9)
        broker.inventory['AAA'] = Inventory(20, 0.1)
        sell = broker.sell('AAA', 0.1, 10)
        self.assertEqual(sell, True)
        self.assertEqual(broker.inventory['AAA'].price, 0.1)
        self.assertEqual(broker.inventory['AAA'].number, 10)
        self.assertEqual(broker.cash, 10000 + 1 - 3.9)
        sell = broker.sell('AAA', 0.2, 10)
        self.assertEqual(sell, True)
        self.assertEqual(broker.inventory['AAA'].price, 0.2)
        self.assertEqual(broker.inventory['AAA'].number, 0)
        self.assertEqual(broker.cash, 10000 + 1 - 3.9 + 2 - 3.9)

    def test_sell_insufficient_inventory(self):
        broker = BrokerBO(cash=10)
        sell = broker.sell('AAA', 10, 10)
        self.assertEqual(sell, False)

    def test_funds(self):
        broker = BrokerBO(cash=10)
        broker.inventory['AAA'] = Inventory(10, 0.1)
        broker.inventory['BBB'] = Inventory(20, 0.2)
        self.assertEqual(broker.funds(), 10 + 10 * 0.1 + 20 * 0.2)


if __name__ == '__main__':
    unittest.main()
