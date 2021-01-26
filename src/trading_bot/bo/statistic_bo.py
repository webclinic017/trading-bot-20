from datetime import datetime
from decimal import Decimal
from typing import List, Dict

from trading_bot.enums.action_enum import ActionEnum


class StatisticBO:

    def __init__(self, name: str = 'statistic') -> None:
        self.name: str = name
        self.__test_data: List[Dict[str, any]] = []
        self.__log_data: List[Dict[str, any]] = []

    def plot(self, date: datetime, symbol: str, price: Decimal, buy: bool, sell: bool) -> None:
        pass  # Do nothing

    def test(self, action: ActionEnum, number: Decimal, symbol: str, price: Decimal) -> None:
        self.__test_data.append({'action': action, 'number': number, 'symbol': symbol, 'price': price})

    def log(self, **kwargs) -> None:
        self.__log_data.append(kwargs)

    @property
    def test_data(self) -> List[Dict[str, any]]:
        return self.__test_data

    def log_data_without_action_none(self) -> List[Dict[str, any]]:
        return list(filter(lambda element: 'strategy' in element or element['action'] is not ActionEnum.NONE,
                           self.__log_data))
