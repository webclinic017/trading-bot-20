from multiprocessing.context import Process
from time import sleep

from requests import Response, get
from requests.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError


class Start:

    @staticmethod
    def request():
        status_code: int = 0
        while status_code != 200:
            sleep(1)
            try:
                response: Response = get('http://127.0.0.1:5000/process/start/schedule')
            except NewConnectionError:
                continue
            except ConnectionError:
                continue
            status_code = 0 if response is None else response.status_code


if __name__ == '__main__':
    process = Process(name='scheduler', target=Start.request)
    process.start()
