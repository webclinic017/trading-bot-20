import unittest
from unittest.suite import TestSuite

from tests.bo.analyser_bo_test import AnalyserBOTestCase
from tests.bo.broker_bo_test import BrokerBOTestCase
from tests.bo.forward_bo_test import ForwardBOTestCase
from tests.bo.inventory_bo_test import InventoryBOTestCase
from tests.bo.optimizer_bo_test import OptimizerBOTestCase
from tests.bo.stock_bo_test import StockBOTestCase
from tests.bo.strategy_bo_test import StrategyBOTestCase
from tests.dao.evaluation_dao_test import EvaluationDAOTestCase
from tests.dao.forward_dao_test import ForwardDAOTestCase
from tests.dao.intraday_dao_test import IntraDayDAOTestCase
from tests.dao.stock_dao_test import StockDAOTestCase
from tests.dto.attempt_dto_test import AttemptDTOTestCase
from tests.main_test import MainTestCase
from tests.process_manager_test import ProcessManagerTestCase
from tests.utils.utils_test import UtilsTestCase

loader = unittest.TestLoader()
suite: TestSuite = unittest.TestSuite()

tests = [AnalyserBOTestCase,
         AttemptDTOTestCase,
         BrokerBOTestCase,
         EvaluationDAOTestCase,
         ForwardDAOTestCase,
         ForwardBOTestCase,
         IntraDayDAOTestCase,
         InventoryBOTestCase,
         StockBOTestCase,
         MainTestCase,
         OptimizerBOTestCase,
         ProcessManagerTestCase,
         StockDAOTestCase,
         StrategyBOTestCase,
         UtilsTestCase]

for test in tests:
    suite.addTests(loader.loadTestsFromTestCase(test))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
