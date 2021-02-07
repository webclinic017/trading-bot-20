from datetime import datetime
from decimal import Decimal
from typing import Dict, List

from trading_bot.bo.broker_bo import BrokerBO
from trading_bot.bo.intraday_bo import IntradayBO
from trading_bot.bo.statistic_bo import StatisticBO
from trading_bot.dto.attempt_dto import AttemptDTO
from trading_bot.entity.intraday_entity import IntradayEntity
from trading_bot.enums.action_enum import ActionEnum
from trading_bot.enums.strategy_enum import StrategyEnum


class AnalyserBO:

    @staticmethod
    def analyse(intraday_list: List[IntradayEntity], strategy: StrategyEnum, broker: BrokerBO,
                statistic: StatisticBO = None, attempt: AttemptDTO = None,
                latest_date_dict: Dict[str, str] = None) -> StatisticBO:
        statistic.log(strategy=strategy)
        intraday_list = IntradayBO.sort_by_date(intraday_list)
        grouped: Dict[str, List[IntradayEntity]] = IntradayBO.group_by_symbol(intraday_list)
        for index, intraday in enumerate(intraday_list):
            symbol: str = intraday.symbol
            date: datetime = intraday.date
            if latest_date_dict is not None and latest_date_dict[symbol] != date:
                continue
            price: Decimal = intraday.close
            action, number = strategy.function(grouped[symbol][:index + 1], date, attempt)
            buy: bool = False
            sell: bool = False
            if action is ActionEnum.BUY:
                buy = broker.buy(symbol, price, number)
            elif action is ActionEnum.SELL:
                sell = broker.sell(symbol, price, number)
            broker.update(symbol, price)
            if statistic is not None:
                statistic.plot(date, symbol, price, buy, sell)
                statistic.test(action, number, symbol, price)
                statistic.log(action=action, date=date, symbol=symbol, price=price)
        return statistic
