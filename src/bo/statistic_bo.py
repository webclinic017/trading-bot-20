from datetime import datetime
from decimal import Decimal
from typing import List, Dict, NoReturn

from src.enums.action_enum import ActionEnum


class StatisticBO:

    def __init__(self, name: str = 'statistic') -> NoReturn:
        self.name: str = name
        self.__test_data: List[Dict[str, any]] = []
        self.__log_data: List[Dict[str, any]] = []

    def plot(self, date: datetime, ticker: str, price: Decimal, buy: bool, sell: bool) -> NoReturn:
        pass  # Do nothing

    def test(self, action: ActionEnum, number: Decimal, ticker: str, price: Decimal) -> NoReturn:
        self.__test_data.append({'action': action, 'number': number, 'ticker': ticker, 'price': price})

    def log(self, action: ActionEnum, date: datetime, ticker: str, price: Decimal) -> NoReturn:
        self.__log_data.append({'action': action, 'date': date, 'ticker': ticker, 'price': price})

    @property
    def test_data(self):
        return self.__test_data

    def log_data_without_action_none(self):
        return list(filter(lambda element: element['action'] is not ActionEnum.NONE, self.__log_data))
