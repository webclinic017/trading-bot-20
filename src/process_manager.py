import multiprocessing


class ProcessManager:

    def __init__(self, ):
        self._processes = []

    def start(self, name, target, args):
        process = multiprocessing.Process(name=name, target=target, args=args)
        process.start()
        self._processes.append(process)

    def stop(self, process_name):
        processes = list(filter(lambda p: p.name == process_name, self.get_processes()))
        for process in processes:
            self._processes.remove(process)
            process.join()
            process.terminate()

    def running(self):
        return any(process.is_alive() for process in self.get_processes())

    def contains(self, process_name):
        return any(process.name == process_name for process in self.get_processes())

    def get_processes(self):
        self._processes = list(filter(lambda process: process.is_alive(), self._processes))
        return self._processes
