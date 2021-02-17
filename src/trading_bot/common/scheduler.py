from logging import warning
from time import sleep

from requests import get
from schedule import every, run_pending


class Scheduler:

    @staticmethod
    def update_table_intraday():
        warning('Scheduler update_table_intraday')
        get('http://127.0.0.1:5000/process/start/update-table-intraday')

    @staticmethod
    def optimize():
        warning('Scheduler optimize')
        get('http://127.0.0.1:5000/process/start/optimize')

    @staticmethod
    def forward():
        warning('Scheduler forward')
        get('http://127.0.0.1:5000/process/start/forward')

    @staticmethod
    def init_database():
        warning('Scheduler init database')
        get('http://127.0.0.1:5000/process/start/init-database')

    @staticmethod
    def fit():
        warning('Scheduler fit')
        get('http://127.0.0.1:5000/process/start/fit')

    @classmethod
    def start(cls) -> None:
        warning('Scheduler start')
        cls.init_database()
        every(9).minutes.do(cls.update_table_intraday)
        every(5).minutes.do(cls.optimize)
        every(5).minutes.do(cls.forward)
        every().day.at('18:00').do(cls.fit)
        while True:
            run_pending()
            sleep(1)
