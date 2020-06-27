import math
from typing import Tuple

from pandas import DataFrame

from src.action import Action
from src.attempt import Attempt
from src.utils import Utils


class Strategy:
    # noinspection DuplicatedCode
    @staticmethod
    def counter_cyclical(frame: DataFrame, i: int, j: int, attempt: Attempt) -> Tuple[Action, float]:
        end_close: float = frame.iloc[i][j]
        if attempt is None:
            attempt = Attempt()
        if i >= attempt.distance_buy:
            start_close: float = frame.iloc[i - attempt.distance_buy][j]
            percent: float = start_close / end_close
            if not math.isnan(start_close) and not math.isnan(end_close) and percent > attempt.delta_buy:
                return Action.BUY, Utils.number(attempt.amount_buy, end_close)
        if i >= attempt.distance_sell:
            start_close: float = frame.iloc[i - attempt.distance_sell][j]
            percent: float = end_close / start_close
            if not math.isnan(start_close) and not math.isnan(end_close) and percent > attempt.delta_sell:
                return Action.SELL, Utils.number(attempt.amount_sell, end_close)
        return Action.NONE, 0
