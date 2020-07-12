import multiprocessing
from multiprocessing.context import Process
from typing import Dict, List, Tuple, Any, Optional

from src.bo.forward_bo import ForwardBO
from src.bo.intraday_bo import IntradayBO
from src.bo.optimizer_bo import OptimizerBO
from src.dao.stock_dao import StockDAO
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
            TARGET: IntradayBO.update,
            ARGS: Portfolio.test_prod_portfolio()
        },
        'schedule': {
            TARGET: Scheduler.start,
            ARGS: []
        },
        'optimize': {
            TARGET: OptimizerBO.start,
            ARGS: (Portfolio.test_portfolio(), 100, 4)
        },
        'forward': {
            TARGET: ForwardBO.start,
            ARGS: []
        }
    }

    @staticmethod
    def start(name: str) -> bool:
        if name in ProcessManager.CONFIGURATION.keys():
            configuration: Dict[str, Tuple[Any, ...]] = ProcessManager.CONFIGURATION.get(name)
            process: Process = ProcessManager.__find(name)
            if process is None or not process.is_alive():
                process = multiprocessing.Process(name=name, target=configuration.get(ProcessManager.TARGET),
                                                  args=configuration.get(ProcessManager.ARGS))
                process.start()
                return True
        return False

    @staticmethod
    def stop(name: str) -> bool:
        if name in ProcessManager.CONFIGURATION.keys():
            process: Process = ProcessManager.__find(name)
            if process is not None:
                process.terminate()
                process.join()
                return True
        return False

    @staticmethod
    def running() -> bool:
        return len(multiprocessing.active_children()) > 0

    @staticmethod
    def get_active_names() -> List[str]:
        return sorted(list(map(lambda p: p.name, list(multiprocessing.active_children()))))

    @staticmethod
    def get_inactive_names() -> List[str]:
        return sorted(list(filter(lambda p: p not in ProcessManager.get_active_names(),
                                  ProcessManager.CONFIGURATION.keys())))

    @staticmethod
    def __find(name) -> Optional[Process]:
        return next(iter(filter(lambda p: p.name == name, multiprocessing.active_children())), None)
