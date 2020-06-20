import random
from typing import Iterable, List, Iterator, Tuple


class Utils:
    @staticmethod
    def valid(start: float, value: float, stop: float) -> bool:
        return start <= value <= stop

    @staticmethod
    def negation() -> int:
        return 1 if random.random() < 0.5 else -1

    @staticmethod
    def inverse() -> float:
        return random.random() if random.random() < 0.5 else 1 / random.random()

    @staticmethod
    def group(n: int, iterable: List[str]) -> Tuple[Tuple[str]]:
        args: Iterable[Iterator] = [iter(iterable)] * n
        return tuple(zip(*args))
