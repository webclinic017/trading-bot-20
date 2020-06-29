import math
import random
from datetime import timedelta, datetime
from typing import Iterable, List, Iterator, Tuple

import pandas as pd
from pandas import DataFrame


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

    @staticmethod
    def day_delta_value(frame: DataFrame, column: str, date: datetime, delta: int) -> float:
        converted = pd.to_datetime(date)
        interval_end = converted - timedelta(days=delta + 7)
        interval_start = converted - timedelta(days=delta)
        interval_date = frame.loc[interval_start:interval_end, column].index.max()
        if pd.isnull(interval_date):
            return math.nan
        return frame.at[interval_date, column]

    @staticmethod
    def is_today(today: datetime) -> bool:
        return False if today is None else Utils.now().date() == today.date()

    @staticmethod
    def now() -> datetime:
        return datetime.now()
