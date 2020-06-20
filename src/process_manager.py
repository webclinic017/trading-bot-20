import multiprocessing
from multiprocessing.context import Process
from typing import List, Optional, Tuple, Any


class ProcessManager:

    def __init__(self) -> None:
        self._processes: List[object] = []

    def start(self, name: str, target: callable, args: Optional[Tuple[Any, ...]]) -> None:
        process: Process = multiprocessing.Process(name=name, target=target, args=args)
        process.start()
        self._processes.append(process)

    def stop(self, process_name: str) -> None:
        processes: List[Process] = list(filter(lambda p: p.name == process_name, self.get_processes()))
        for process in processes:
            self._processes.remove(process)
            process.join()
            process.terminate()

    def running(self) -> bool:
        return any(process.is_alive() for process in self.get_processes())

    def contains(self, process_name: str) -> bool:
        return any(process.name == process_name for process in self.get_processes())

    def get_processes(self) -> List[Process]:
        self._processes = list(filter(lambda process: process.is_alive(), self._processes))
        return self._processes
