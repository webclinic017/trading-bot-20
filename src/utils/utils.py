import random
from datetime import timedelta, datetime
from decimal import Decimal, ROUND_DOWN, ExtendedContext
from typing import Iterable, List, Iterator, Tuple, Optional, TypeVar, Sequence

import pandas as pd
import pytz
from pandas import DataFrame
from workalendar.usa import NewYork

from src.constants import US_EASTERN, ZERO, NAN

T = TypeVar('T')


class Utils:
    @staticmethod
    def valid(start: Decimal, value: Decimal, stop: Decimal) -> bool:
        return start <= value <= stop

    @staticmethod
    def negation() -> Decimal:
        return Decimal('1') if random.random() < 0.5 else Decimal('-1')

    @staticmethod
    def inverse() -> Decimal:
        return Decimal(random.random()) if random.random() < 0.5 else Decimal(1 / (1 - random.random()))

    @staticmethod
    def group(number: int, iterable: List[T]) -> Tuple[Tuple[T]]:
        args: Iterable[Iterator] = [iter(iterable)] * number
        return tuple(zip(*args))

    @staticmethod
    def number(numerator: Decimal, denominator: Decimal) -> Decimal:
        return ZERO if denominator == ZERO else ExtendedContext.divide_int(numerator, denominator)

    @staticmethod
    def day_delta_value(frame: DataFrame, column: str, date: datetime, delta: Decimal) -> Decimal:
        interval_end = date - timedelta(days=float(delta))
        interval_start = date - timedelta(days=float(delta) + 7)
        interval_date = frame.loc[interval_start:interval_end, column].index.max()
        if pd.isnull(interval_date):
            return NAN
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

    @staticmethod
    def first(sequence: Sequence[T]) -> T:
        return None if len(sequence) == 0 else sequence[0]

    @staticmethod
    def set_attributes(assignable: object, **kwargs: any) -> None:
        for key, value in kwargs.items():
            setattr(assignable, key, value)

    @staticmethod
    def truncate(number: Decimal) -> None:
        return Decimal(number).quantize(Decimal('1'), rounding=ROUND_DOWN)
