import math
from datetime import datetime
from decimal import Decimal
from typing import Tuple

from pandas import DataFrame

from src.constants import ZERO
from src.dto.attempt_dto import AttemptDTO
from src.enums.action_enum import ActionEnum
from src.utils.utils import Utils


class StrategyBO:
    # noinspection DuplicatedCode
    @staticmethod
    def counter_cyclical(frame: DataFrame, ticker: str, date: datetime,
                         attempt: AttemptDTO) -> Tuple[ActionEnum, Decimal]:
        end_close: Decimal = frame.at[date, ticker]
        if attempt is None:
            attempt = AttemptDTO()
        start_close: Decimal = Utils.day_delta_value(frame, ticker, date, attempt.distance_buy)
        if not math.isnan(start_close):
            percent: Decimal = start_close / end_close
            if not math.isnan(start_close) and not math.isnan(end_close) and percent > attempt.delta_buy:
                return ActionEnum.BUY, Utils.number(attempt.amount_buy, end_close)
        start_close: Decimal = Utils.day_delta_value(frame, ticker, date, attempt.distance_sell)
        if not math.isnan(start_close):
            percent: Decimal = end_close / start_close
            if not math.isnan(start_close) and not math.isnan(end_close) and percent > attempt.delta_sell:
                return ActionEnum.SELL, Utils.number(attempt.amount_sell, end_close)
        return ActionEnum.NONE, ZERO
