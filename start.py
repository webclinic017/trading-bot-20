import time
from multiprocessing.context import Process

import requests


class Start:

    @staticmethod
    def request():
        status_code = 0
        while status_code != 200:
            time.sleep(1)
            response = requests.get('http://127.0.0.1:5000/process/start/schedule')
            status_code = 0 if response is None else response.status_code


if __name__ == '__main__':
    process = Process(name='scheduler', target=Start.request)
    process.start()
