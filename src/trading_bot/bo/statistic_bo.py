from typing import List, Dict

from trading_bot.enums.action_enum import ActionEnum


class StatisticBO:

    def __init__(self, name: str = 'statistic') -> None:
        self.name: str = name
        self.__test_data: List[Dict[str, any]] = []
        self.__log_data: List[Dict[str, any]] = []

    def plot(self, **kwargs) -> None:
        pass  # Do nothing

    def test(self, **kwargs) -> None:
        self.__test_data.append(kwargs)

    def log(self, **kwargs) -> None:
        self.__log_data.append(kwargs)

    @property
    def test_data(self) -> List[Dict[str, any]]:
        return self.__test_data

    def log_data_without_action_none(self) -> List[Dict[str, any]]:
        return list(filter(lambda element: 'strategy' in element or element['action'] is not ActionEnum.NONE,
                           self.__log_data))
