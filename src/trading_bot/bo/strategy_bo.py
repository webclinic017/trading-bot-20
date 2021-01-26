import math
from datetime import datetime
from decimal import Decimal
from typing import Tuple, List, Callable

from pandas import DataFrame
from predictor.dto.prediction_dto import PredictionDTO

from trading_bot.common.constants import ZERO
from trading_bot.common.predictor_adapter import PredictorAdapter
from trading_bot.converter.intraday_entity_converter import IntradayEntityConverter
from trading_bot.dto.attempt_dto import AttemptDTO
from trading_bot.entity.intraday_entity import IntradayEntity
from trading_bot.enums.action_enum import ActionEnum
from trading_bot.utils.utils import Utils

Strategy = Callable[[List[IntradayEntity], datetime, AttemptDTO], Tuple[ActionEnum, Decimal]]


class StrategyBO:
    # noinspection DuplicatedCode
    @staticmethod
    def counter_cyclical(intraday_list: List[IntradayEntity], date: datetime,
                         attempt: AttemptDTO) -> Tuple[ActionEnum, Decimal]:
        frame: DataFrame = IntradayEntityConverter.to_dataframe(intraday_list)
        close: Decimal = frame.at[date, frame.columns[0]]
        normalized: DataFrame = Utils.normalize(frame)
        end_close: Decimal = normalized.at[date, normalized.columns[0]]
        if attempt is None:
            attempt = AttemptDTO()
        start_close: Decimal = Utils.day_delta_value(normalized, date, attempt.distance_buy)
        if not math.isnan(start_close):
            percent: Decimal = start_close - end_close
            if not math.isnan(start_close) and not math.isnan(end_close) and percent > attempt.delta_buy:
                return ActionEnum.BUY, Utils.number(attempt.amount_buy, close)
        start_close: Decimal = Utils.day_delta_value(normalized, date, attempt.distance_sell)
        if not math.isnan(start_close):
            percent: Decimal = end_close - start_close
            if not math.isnan(start_close) and not math.isnan(end_close) and percent > attempt.delta_sell:
                return ActionEnum.SELL, Utils.number(attempt.amount_sell, close)
        return ActionEnum.NONE, ZERO

    # noinspection DuplicatedCode
    @staticmethod
    def volume_trading(intraday_list: List[IntradayEntity], date: datetime,
                       attempt: AttemptDTO) -> Tuple[ActionEnum, Decimal]:
        frame: DataFrame = IntradayEntityConverter.to_dataframe(intraday_list, column='volume')
        close: Decimal = frame.at[date, frame.columns[0]]
        normalized: DataFrame = Utils.normalize(frame)
        end_volume: Decimal = normalized.at[date, normalized.columns[0]]
        if attempt is None:
            attempt = AttemptDTO()
        start_volume: Decimal = Utils.day_delta_value(normalized, date, attempt.distance_buy)
        if not math.isnan(start_volume):
            percent: Decimal = start_volume - end_volume
            if not math.isnan(start_volume) and not math.isnan(end_volume) and percent > attempt.delta_buy:
                return ActionEnum.BUY, Utils.number(attempt.amount_buy, close)
        start_volume: Decimal = Utils.day_delta_value(normalized, date, attempt.distance_sell)
        if not math.isnan(start_volume):
            percent: Decimal = end_volume - start_volume
            if not math.isnan(start_volume) and not math.isnan(end_volume) and percent > attempt.delta_sell:
                return ActionEnum.SELL, Utils.number(attempt.amount_sell, close)
        return ActionEnum.NONE, ZERO

    @staticmethod
    def predictor(intraday_list: List[IntradayEntity], date: datetime,
                  attempt: AttemptDTO) -> Tuple[ActionEnum, Decimal]:
        close: Decimal = list(filter(lambda i: i.date == date, intraday_list))[0].close
        prediction: PredictionDTO = PredictorAdapter.predict(intraday_list)
        if prediction is None or math.isnan(prediction.delta):
            return ActionEnum.NONE, ZERO
        if Decimal(prediction.delta) > attempt.delta_buy:
            return ActionEnum.BUY, Utils.number(attempt.amount_buy, close)
        if Decimal(prediction.delta) < attempt.delta_sell:
            return ActionEnum.SELL, Utils.number(attempt.amount_sell, close)
        return ActionEnum.NONE, ZERO
