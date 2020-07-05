import unittest
from unittest.suite import TestSuite

from tests.analyser_test import AnalyserTestCase
from tests.attempt_test import AttemptTestCase
from tests.broker_test import BrokerTestCase
from tests.evaluation_dao_test import EvaluationDAOTestCase
from tests.forward_dao_test import ForwardDAOTestCase
from tests.intraday_dao_test import IntraDayDAOTestCase
from tests.inventory_test import InventoryTestCase
from tests.optimizer_test import OptimizerTestCase
from tests.process_manager_test import ProcessManagerTestCase
from tests.stock_dao_test import StockDAOTestCase
from tests.strategy_test import StrategyTestCase
from tests.utils_test import UtilsTestCase

loader = unittest.TestLoader()
suite: TestSuite = unittest.TestSuite()

tests = [AnalyserTestCase,
         AttemptTestCase,
         BrokerTestCase,
         EvaluationDAOTestCase,
         ForwardDAOTestCase,
         IntraDayDAOTestCase,
         InventoryTestCase,
         OptimizerTestCase,
         ProcessManagerTestCase,
         StockDAOTestCase,
         StrategyTestCase,
         UtilsTestCase]

for test in tests:
    suite.addTests(loader.loadTestsFromTestCase(test))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
