import multiprocessing
from multiprocessing.context import Process
from typing import Dict, List, Tuple, Any

from src.dao.intraday_dao import IntradayDAO
from src.dao.stock_dao import StockDAO
from src.forward import Forward
from src.optimizer import Optimizer
from src.portfolio import Portfolio
from src.scheduler import Scheduler


class ProcessManager:
    TARGET: str = 'target'
    ARGS: str = 'args'

    CONFIGURATION: Dict[str, Dict[str, Tuple[Any, ...]]] = {
        'update-table-stock': {
            TARGET: StockDAO.update,
            ARGS: Portfolio.test_prod_portfolio()
        },
        'update-table-intraday': {
            TARGET: IntradayDAO.update,
            ARGS: Portfolio.test_prod_portfolio()
        },
        'schedule': {
            TARGET: Scheduler.start,
            ARGS: []
        },
        'optimize': {
            TARGET: Optimizer.start,
            ARGS: (Portfolio.test_portfolio(), 100, 4)
        },
        'forward': {
            TARGET: Forward.start,
            ARGS: []
        }
    }

    def __init__(self) -> None:
        self.__processes: Dict[str, Process] = dict()

    @property
    def get_processes(self):
        return self.__processes

    def start(self, name: str) -> bool:
        if name in ProcessManager.CONFIGURATION.keys():
            configuration: Dict[str, Tuple[Any, ...]] = ProcessManager.CONFIGURATION.get(name)
            process: Process = self.__processes.get(name)
            if process is None or not process.is_alive():
                process = multiprocessing.Process(name=name, target=configuration.get(ProcessManager.TARGET),
                                                  args=configuration.get(ProcessManager.ARGS))
                process.start()
                self.__processes[name] = process
                return True
        return False

    def stop(self, name: str) -> bool:
        if name in ProcessManager.CONFIGURATION.keys():
            process: Process = self.__processes.get(name)
            process.terminate()
            process.join()
            del self.__processes[name]
            return True
        return False

    def running(self) -> bool:
        return len(self.__processes) > 0

    def get_active_names(self) -> List[str]:
        return list(self.__processes)

    def get_inactive_names(self) -> List[str]:
        return list(filter(lambda j: j not in list(self.__processes), ProcessManager.CONFIGURATION.keys()))
