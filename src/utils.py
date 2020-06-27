import math
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
        return random.random() if random.random() < 0.5 else 1 / (1 - random.random())

    @staticmethod
    def group(number: int, iterable: List[any]) -> Tuple[Tuple[str]]:
        args: Iterable[Iterator] = [iter(iterable)] * number
        return tuple(zip(*args))

    @staticmethod
    def number(numerator: float, denominator: float) -> float:
        return 0 if denominator == 0 else math.floor(numerator / denominator)
