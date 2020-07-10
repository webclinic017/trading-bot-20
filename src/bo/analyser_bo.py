from datetime import datetime
from typing import Dict

import pandas as pd
from numpy import datetime64
from pandas import DataFrame

from src.bo.broker_bo import BrokerBO
from src.bo.statistic_bo import StatisticBO
from src.dto.attempt_dto import AttemptDTO
from src.enums.action_enum import ActionEnum


class AnalyserBO:
    @staticmethod
    def analyse(frame: DataFrame, strategy: callable, broker: BrokerBO, statistic: StatisticBO = None,
                attempt: AttemptDTO = None, latest_date_dict: Dict[str, str] = None) -> StatisticBO:
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                ticker: str = frame.columns[j]
                date: datetime64 = frame.index.values[i]
                current_date: datetime = pd.to_datetime(date, format='%d%b%Y:%H:%M:%S.%f')
                if latest_date_dict is not None and latest_date_dict[ticker] != current_date:
                    continue
                price: float = frame.iloc[i][j]
                action, number = strategy(frame, ticker, date, attempt)
                buy: bool = False
                sell: bool = False
                if action == ActionEnum.BUY:
                    buy = broker.buy(ticker, price, number)
                elif action == ActionEnum.SELL:
                    sell = broker.sell(ticker, price, number)
                else:
                    broker.update(ticker, price)
                if statistic is not None:
                    statistic.plot(current_date, ticker, price, buy, sell)
                    statistic.test(action, number, ticker, price)
                    statistic.log(action, current_date, ticker, price, buy, sell)
        return statistic
