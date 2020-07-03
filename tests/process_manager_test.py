import unittest
from unittest.mock import patch

from src.process_manager import ProcessManager


class ProcessManagerTestCase(unittest.TestCase):
    class TestProcess:
        @staticmethod
        def test():
            pass

    configuration = {
        'test1': {
            ProcessManager.TARGET: TestProcess.test(),
            ProcessManager.ARGS: []
        },
        'test2': {
            ProcessManager.TARGET: TestProcess.test(),
            ProcessManager.ARGS: []
        }
    }

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_successful(self):
        manager = ProcessManager()
        self.__start(manager, 'test1', True, True, ['test1'], ['test2'])
        self.__start(manager, 'test1', False, True, ['test1'], ['test2'])
        self.__stop(manager, 'test1', True, False, [], ['test1', 'test2'])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_successful_twice(self):
        manager = ProcessManager()
        self.__start(manager, 'test1', True, True, ['test1'], ['test2'])
        self.__stop(manager, 'test1', True, False, [], ['test1', 'test2'])
        self.__start(manager, 'test1', True, True, ['test1'], ['test2'])
        self.__stop(manager, 'test1', True, False, [], ['test1', 'test2'])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_successful_with_second(self):
        manager = ProcessManager()
        self.__start(manager, 'test1', True, True, ['test1'], ['test2'])
        self.__start(manager, 'test2', True, True, ['test1', 'test2'], [])
        self.__stop(manager, 'test2', True, True, ['test1'], ['test2'])
        self.__stop(manager, 'test1', True, False, [], ['test1', 'test2'])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_successful_wait(self):
        manager = ProcessManager()
        self.__start(manager, 'test1', True, True, ['test1'], ['test2'])
        while manager.get_processes['test1'].is_alive():
            pass
        self.__start(manager, 'test1', True, True, ['test1'], ['test2'])
        self.__stop(manager, 'test1', True, False, [], ['test1', 'test2'])

    @patch('src.process_manager.ProcessManager.CONFIGURATION', new=configuration)
    def test_failed(self):
        manager = ProcessManager()
        self.__start(manager, '', False, False, [], ['test1', 'test2'])
        self.__stop(manager, '', False, False, [], ['test1', 'test2'])

    def __start(self, manager, name, successful, running, active_names, inactive_names):
        self.assertEqual(manager.start(name), successful)
        self.assertEqual(manager.running(), running)
        self.assertEqual(manager.get_active_names(), active_names)
        self.assertEqual(manager.get_inactive_names(), inactive_names)

    def __stop(self, manager, name, successful, running, active_names, inactive_names):
        self.assertEqual(manager.stop(name), successful)
        self.assertEqual(manager.running(), running)
        self.assertEqual(manager.get_active_names(), active_names)
        self.assertEqual(manager.get_inactive_names(), inactive_names)


if __name__ == '__main__':
    unittest.main()
