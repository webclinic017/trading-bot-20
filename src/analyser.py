from typing import Dict

from pandas import DataFrame

from src.attempt import Attempt
from src.broker import Broker
from src.constants import BUY, SELL
from src.statistic import Statistic


class Analyser:
    @staticmethod
    def analyse(frame: DataFrame, strategy: callable, broker: Broker, statistic: Statistic = None,
                attempt: Attempt = None, latest_date_dict: Dict[str, str] = None) -> Statistic:
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                ticker: str = frame.columns[j]
                date: str = frame.index.values[i]
                if latest_date_dict is not None and latest_date_dict[ticker] != date:
                    continue
                price: float = frame.iloc[i][j]
                action, number = strategy(frame, i, j, attempt)
                buy: bool = False
                sell: bool = False
                if action == BUY:
                    buy = broker.buy(ticker, price, number)
                elif action == SELL:
                    sell = broker.sell(ticker, price, number)
                else:
                    broker.update(ticker, price)
                if statistic is not None:
                    statistic.plot(date, ticker, price, buy, sell)
                    statistic.test(action, number, ticker, broker)
                    statistic.log(action, date, ticker, price, buy, sell)
        return statistic
