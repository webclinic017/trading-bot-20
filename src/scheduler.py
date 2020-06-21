import time

import requests
import schedule


class Scheduler:

    @staticmethod
    def update_table_intraday():
        requests.get('http://127.0.0.1:5000/process/start/update-table-intraday')

    @staticmethod
    def optimize():
        requests.get('http://127.0.0.1:5000/process/start/optimize')

    @staticmethod
    def forward():
        requests.get('http://127.0.0.1:5000/process/start/forward')

    @staticmethod
    def start() -> None:
        schedule.every(10).seconds.do(Scheduler.update_table_intraday)
        schedule.every(10).seconds.do(Scheduler.optimize)
        schedule.every(10).seconds.do(Scheduler.forward)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    Scheduler.start()
