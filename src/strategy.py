import math
from datetime import datetime
from typing import Tuple

from pandas import DataFrame

from src.action import Action
from src.attempt import Attempt
from src.utils import Utils


class Strategy:
    # noinspection DuplicatedCode
    @staticmethod
    def counter_cyclical(frame: DataFrame, ticker: str, date: datetime, attempt: Attempt) -> Tuple[Action, float]:
        end_close: float = frame.at[date, ticker]
        if attempt is None:
            attempt = Attempt()
        start_close: float = Utils.day_delta_value(frame, ticker, date, attempt.distance_buy)
        if not math.isnan(start_close):
            percent: float = start_close / end_close
            if not math.isnan(start_close) and not math.isnan(end_close) and percent > attempt.delta_buy:
                return Action.BUY, Utils.number(attempt.amount_buy, end_close)
        start_close: float = Utils.day_delta_value(frame, ticker, date, attempt.distance_sell)
        if not math.isnan(start_close):
            percent: float = end_close / start_close
            if not math.isnan(start_close) and not math.isnan(end_close) and percent > attempt.delta_sell:
                return Action.SELL, Utils.number(attempt.amount_sell, end_close)
        return Action.NONE, 0
