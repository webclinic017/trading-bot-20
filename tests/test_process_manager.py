import multiprocessing
import time
import unittest
from unittest.mock import patch

from src.bo.forward_bo import ForwardBO
from src.bo.intraday_bo import IntradayBO
from src.bo.optimization_bo import OptimizationBO
from src.dao.stock_dao import StockDAO
from src.portfolio import Portfolio
from src.process_manager import ProcessManager
from src.scheduler import Scheduler


class ProcessManagerTestCase(unittest.TestCase):
    class TestProcess:
        @staticmethod
        def test():
            time.sleep(1)

    configuration = {
        'test1': {
            ProcessManager.TARGET: TestProcess.test,
            ProcessManager.ARGS: []
        },
        'test2': {
            ProcessManager.TARGET: TestProcess.test,
            ProcessManager.ARGS: []
        }
    }

    def test_configuration(self):
        names = ['update-table-stock', 'update-table-intraday', 'schedule', 'optimize', 'forward']
        self.assertListEqual(list(ProcessManager.CONFIGURATION.keys()), names)
        update_table_stock = ProcessManager.CONFIGURATION['update-table-stock']
        self.assertEqual(update_table_stock[ProcessManager.TARGET], StockDAO.update)
        self.assertEqual(update_table_stock[ProcessManager.ARGS], (Portfolio.test_prod_portfolio(),))
        update_table_intraday = ProcessManager.CONFIGURATION['update-table-intraday']
        self.assertEqual(update_table_intraday[ProcessManager.TARGET], IntradayBO.update)
        self.assertEqual(update_table_intraday[ProcessManager.ARGS], (Portfolio.test_prod_portfolio(),))
        schedule = ProcessManager.CONFIGURATION['schedule']
        self.assertEqual(schedule[ProcessManager.TARGET], Scheduler.start)
        self.assertEqual(schedule[ProcessManager.ARGS], [])
        optimize = ProcessManager.CONFIGURATION['optimize']
        self.assertEqual(optimize[ProcessManager.TARGET], OptimizationBO.start)
        self.assertEqual(optimize[ProcessManager.ARGS], (Portfolio.test_portfolio(), 100, 4))
        forward = ProcessManager.CONFIGURATION['forward']
        self.assertEqual(forward[ProcessManager.TARGET], ForwardBO.start)
        self.assertEqual(forward[ProcessManager.ARGS], [])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_successful(self):
        self.__start('test1', True, True, ['test1'], ['test2'])
        self.__start('test1', False, True, ['test1'], ['test2'])
        self.__stop('test1', True, False, [], ['test1', 'test2'])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_successful_twice(self):
        self.__stop('test1', False, False, [], ['test1', 'test2'])
        self.__start('test1', True, True, ['test1'], ['test2'])
        self.__stop('test1', True, False, [], ['test1', 'test2'])
        self.__start('test1', True, True, ['test1'], ['test2'])
        self.__stop('test1', True, False, [], ['test1', 'test2'])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_successful_with_second(self):
        self.__start('test1', True, True, ['test1'], ['test2'])
        self.__start('test2', True, True, ['test1', 'test2'], [])
        self.__stop('test2', True, True, ['test1'], ['test2'])
        self.__stop('test1', True, False, [], ['test1', 'test2'])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_successful_wait(self):
        self.__start('test1', True, True, ['test1'], ['test2'])
        while len(multiprocessing.active_children()) > 0:
            pass  # Do nothing
        self.assertEqual(ProcessManager.running(), False)
        self.assertListEqual(ProcessManager.get_active_names(), [])
        self.assertListEqual(ProcessManager.get_inactive_names(), ['test1', 'test2'])
        self.__start('test1', True, True, ['test1'], ['test2'])
        self.__stop('test1', True, False, [], ['test1', 'test2'])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_failed(self):
        self.__start('', False, False, [], ['test1', 'test2'])
        self.__stop('', False, False, [], ['test1', 'test2'])

    def __start(self, name, successful, running, active_names, inactive_names):
        self.assertEqual(ProcessManager.start(name), successful)
        time.sleep(0.1)
        self.assertEqual(ProcessManager.running(), running)
        self.assertListEqual(ProcessManager.get_active_names(), active_names)
        self.assertListEqual(ProcessManager.get_inactive_names(), inactive_names)

    def __stop(self, name, successful, running, active_names, inactive_names):
        self.assertEqual(ProcessManager.stop(name), successful)
        time.sleep(0.1)
        self.assertEqual(ProcessManager.running(), running)
        self.assertListEqual(ProcessManager.get_active_names(), active_names)
        self.assertListEqual(ProcessManager.get_inactive_names(), inactive_names)


if __name__ == '__main__':
    unittest.main()
