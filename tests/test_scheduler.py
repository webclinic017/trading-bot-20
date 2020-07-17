import unittest
from unittest.mock import patch

from src.scheduler import Scheduler


class SchedulerTestCase(unittest.TestCase):

    @patch('requests.get')
    def test_update_table_intraday(self, get):
        Scheduler.update_table_intraday()
        get.assert_called_once_with('http://127.0.0.1:5000/process/start/update-table-intraday')

    @patch('requests.get')
    def test_optimize(self, get):
        Scheduler.optimize()
        get.assert_called_once_with('http://127.0.0.1:5000/process/start/optimize')

    @patch('requests.get')
    def test_forward(self, get):
        Scheduler.forward()
        get.assert_called_once_with('http://127.0.0.1:5000/process/start/forward')

    @patch('schedule.run_pending', side_effect=RuntimeError())
    def test_start(self, run_pending):
        try:
            Scheduler.start()
        except RuntimeError:
            pass
        run_pending.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
