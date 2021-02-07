from unittest import TestCase
from unittest.mock import patch

from trading_bot.common.scheduler import Scheduler


class SchedulerTestCase(TestCase):

    @patch('trading_bot.common.scheduler.get')
    def test_update_table_intraday(self, get):
        Scheduler.update_table_intraday()
        get.assert_called_once_with('http://127.0.0.1:5000/process/start/update-table-intraday')

    @patch('trading_bot.common.scheduler.get')
    def test_optimize(self, get):
        Scheduler.optimize()
        get.assert_called_once_with('http://127.0.0.1:5000/process/start/optimize')

    @patch('trading_bot.common.scheduler.get')
    def test_forward(self, get):
        Scheduler.forward()
        get.assert_called_once_with('http://127.0.0.1:5000/process/start/forward')

    @patch('trading_bot.common.scheduler.get')
    def test_init_database(self, get):
        Scheduler.init_database()
        get.assert_called_once_with('http://127.0.0.1:5000/process/start/init-database')

    @patch('trading_bot.common.scheduler.Scheduler.init_database')
    @patch('trading_bot.common.scheduler.run_pending', side_effect=RuntimeError())
    def test_start(self, init_database, run_pending):
        try:
            Scheduler.start()
        except RuntimeError:
            pass
        init_database.assert_called_once_with()
        run_pending.assert_called_once_with()
