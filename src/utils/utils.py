import math
import random
from datetime import timedelta, datetime
from typing import Iterable, List, Iterator, Tuple, Optional

import pandas as pd
import pytz
from pandas import DataFrame
from workalendar.usa import NewYork

from src.constants import US_EASTERN


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
        interval_end = date - timedelta(days=delta)
        interval_start = date - timedelta(days=delta + 7)
        interval_date = frame.loc[interval_start:interval_end, column].index.max()
        if pd.isnull(interval_date):
            return math.nan
        return frame.at[interval_date, column]

    @staticmethod
    def is_today(today: Optional[datetime]) -> bool:
        return False if not isinstance(today, datetime) else Utils.now().date() == today.date()

    @staticmethod
    def now() -> datetime:
        return pytz.utc.localize(datetime.utcnow())

    @staticmethod
    def is_working_day_ny() -> datetime:
        return NewYork().is_working_day(Utils.now().astimezone(pytz.timezone(US_EASTERN)))
