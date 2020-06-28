import unittest

from tests.analyser_test import AnalyserTestCase
from tests.attempt_test import AttemptTestCase
from tests.broker_test import BrokerTestCase
from tests.intraday_dao_test import IntraDayDAOTestCase
from tests.inventory_test import InventoryTestCase
from tests.stock_dao_test import StockDAOTestCase
from tests.strategy_test import StrategyTestCase
from tests.utils_test import UtilsTestCase

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(AnalyserTestCase))
suite.addTests(loader.loadTestsFromTestCase(AttemptTestCase))
suite.addTests(loader.loadTestsFromTestCase(BrokerTestCase))
suite.addTests(loader.loadTestsFromTestCase(IntraDayDAOTestCase))
suite.addTests(loader.loadTestsFromTestCase(InventoryTestCase))
suite.addTests(loader.loadTestsFromTestCase(StockDAOTestCase))
suite.addTests(loader.loadTestsFromTestCase(StrategyTestCase))
suite.addTests(loader.loadTestsFromTestCase(UtilsTestCase))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
