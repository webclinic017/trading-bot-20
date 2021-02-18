from datetime import datetime
from decimal import Decimal
from itertools import chain
from typing import Dict

from pandas import DataFrame

from trading_bot.bo.broker_bo import BrokerBO
from trading_bot.bo.statistic_bo import StatisticBO
from trading_bot.dto.attempt_dto import AttemptDTO
from trading_bot.enums.action_enum import ActionEnum
from trading_bot.enums.strategy_enum import StrategyEnum


class AnalyserBO:

    @staticmethod
    def analyse(intraday_dict: Dict[str, DataFrame], strategy: StrategyEnum, broker: BrokerBO,
                statistic: StatisticBO = None, attempt: AttemptDTO = None,
                latest_date_dict: Dict[str, str] = None) -> StatisticBO:

        dates = sorted(set(chain(*[j['date'].tolist() for j in intraday_dict.values()])))
        statistic.log(strategy=strategy)
        i = 0
        for end in dates:
            for symbol, intraday in intraday_dict.items():
                sliced: DataFrame = intraday.loc[intraday['date'] <= end]
                if len(sliced) == 0:
                    continue
                date: datetime = sliced['date'][len(sliced) - 1]
                if latest_date_dict is not None and latest_date_dict[symbol] != date:
                    continue
                close: Decimal = Decimal(sliced['close'][len(sliced) - 1])
                action, number = strategy.function(sliced, attempt)
                buy: bool = False
                sell: bool = False
                if action is ActionEnum.BUY:
                    buy = broker.buy(symbol, close, number)
                elif action is ActionEnum.SELL:
                    sell = broker.sell(symbol, close, number)
                broker.update(symbol, close)
                if statistic is not None:
                    statistic.plot(action=date, symbol=symbol, close=close, buy=buy, sell=sell)
                    statistic.test(action=action, number=number, symbol=symbol, price=close)
                    statistic.log(action=action, date=date, symbol=symbol, price=close)
                i += 1
        return statistic
