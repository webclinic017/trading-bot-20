from enum import Enum

from trading_bot.bo.strategy_bo import StrategyBO, Strategy


class StrategyEnum(Enum):
    COUNTER_CYCLICAL = ('COUNTER_CYCLICAL', StrategyBO.counter_cyclical)
    VOLUME_TRADING = ('VOLUME_TRADING', StrategyBO.volume_trading)
    PREDICTOR = ('PREDICTOR', StrategyBO.predictor)

    def __init__(self, identifier: str, function: Strategy):
        self.identifier = identifier
        self.function = function
