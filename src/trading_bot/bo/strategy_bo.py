import math
from datetime import timedelta, datetime
from decimal import Decimal
from typing import Tuple, Callable

from pandas import DataFrame
from predictor.dto.prediction_dto import PredictionDTO

from trading_bot.common.constants import ZERO
from trading_bot.common.predictor_adapter import PredictorAdapter
from trading_bot.dto.attempt_dto import AttemptDTO
from trading_bot.enums.action_enum import ActionEnum
from trading_bot.utils.utils import Utils

Strategy = Callable[[DataFrame, AttemptDTO], Tuple[ActionEnum, Decimal]]


class StrategyBO:
    # noinspection DuplicatedCode
    @staticmethod
    def counter_cyclical(frame: DataFrame, attempt: AttemptDTO) -> Tuple[ActionEnum, Decimal]:
        close: Decimal = Decimal(frame['close'].iloc[len(frame) - 1])
        date: datetime = frame['date'].iloc[len(frame) - 1]

        buy_frame: DataFrame = frame.loc[frame['date'] >= date - timedelta(days=float(attempt.distance_buy))]
        buy_normalized: DataFrame = Utils.normalize(buy_frame[['close', 'high', 'low', 'open', 'volume']])

        sell_frame: DataFrame = frame.loc[frame['date'] >= date - timedelta(days=float(attempt.distance_sell))]
        sell_normalized: DataFrame = Utils.normalize(sell_frame[['close', 'high', 'low', 'open', 'volume']])

        if attempt is None:
            attempt = AttemptDTO()
        if len(buy_normalized) > 0:
            buy_end_close: Decimal = buy_normalized['close'].iloc[len(buy_normalized) - 1]
            buy_start_close: Decimal = buy_normalized['close'].iloc[0]
            if not math.isnan(buy_start_close) and not math.isnan(buy_end_close):
                percent: Decimal = buy_start_close - buy_end_close
                if percent > attempt.delta_buy:
                    return ActionEnum.BUY, Utils.number(attempt.amount_buy, close)
        if len(sell_normalized) > 0:
            sell_end_close: Decimal = sell_normalized['close'].iloc[len(sell_normalized) - 1]
            sell_start_close: Decimal = sell_normalized['close'].iloc[0]
            if not math.isnan(sell_start_close) and not math.isnan(sell_end_close):
                percent: Decimal = sell_end_close - sell_start_close
                if percent > attempt.delta_sell:
                    return ActionEnum.SELL, Utils.number(attempt.amount_sell, close)
        return ActionEnum.NONE, ZERO

    # noinspection DuplicatedCode
    @staticmethod
    def volume_trading(frame: DataFrame, attempt: AttemptDTO) -> Tuple[ActionEnum, Decimal]:
        close: Decimal = Decimal(frame['close'].iloc[len(frame) - 1])
        date: datetime = frame['date'].iloc[len(frame) - 1]

        buy_frame: DataFrame = frame.loc[frame['date'] >= date - timedelta(days=float(attempt.distance_buy))]
        buy_normalized: DataFrame = Utils.normalize(buy_frame[['close', 'high', 'low', 'open', 'volume']])

        sell_frame: DataFrame = frame.loc[frame['date'] >= date - timedelta(days=float(attempt.distance_sell))]
        sell_normalized: DataFrame = Utils.normalize(sell_frame[['close', 'high', 'low', 'open', 'volume']])

        if attempt is None:
            attempt = AttemptDTO()
        if len(buy_normalized) > 0:
            buy_end_close: Decimal = buy_normalized['volume'].iloc[len(buy_normalized) - 1]
            buy_start_close: Decimal = buy_normalized['volume'].iloc[0]
            if not math.isnan(buy_start_close) and not math.isnan(buy_end_close):
                percent: Decimal = buy_start_close - buy_end_close
                if percent > attempt.delta_buy:
                    return ActionEnum.BUY, Utils.number(attempt.amount_buy, close)
        if len(sell_normalized) > 0:
            sell_end_close: Decimal = sell_normalized['volume'].iloc[len(sell_normalized) - 1]
            sell_start_close: Decimal = sell_normalized['volume'].iloc[0]
            if not math.isnan(sell_start_close) and not math.isnan(sell_end_close):
                percent: Decimal = sell_end_close - sell_start_close
                if percent > attempt.delta_sell:
                    return ActionEnum.SELL, Utils.number(attempt.amount_sell, close)
        return ActionEnum.NONE, ZERO

    @staticmethod
    def predictor(frame: DataFrame, attempt: AttemptDTO) -> Tuple[ActionEnum, Decimal]:
        close: Decimal = Decimal(frame['close'].iloc[len(frame) - 1])
        prediction: PredictionDTO = PredictorAdapter.predict(frame)
        if prediction is None or math.isnan(prediction.delta):
            return ActionEnum.NONE, ZERO
        if Decimal(prediction.delta) > attempt.delta_buy:
            return ActionEnum.BUY, Utils.number(attempt.amount_buy, close)
        if Decimal(prediction.delta) < attempt.delta_sell:
            return ActionEnum.SELL, Utils.number(attempt.amount_sell, close)
        return ActionEnum.NONE, ZERO
