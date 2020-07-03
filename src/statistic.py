from datetime import datetime
from typing import List, Dict

from src.broker import Broker
from src.inventory import Inventory


class Statistic:

    def __init__(self, name: str = 'statistic') -> None:
        self.name: str = name
        self.test_data: List[Dict[str, any]] = []

    def plot(self, date: datetime, ticker: str, price: float, buy: bool, sell: bool) -> None:
        pass  # Do nothing

    def test(self, action: str, number: int, ticker: str, broker: Broker) -> None:
        entry: Inventory = broker.inventory.get(ticker)
        data = {'cash': broker.cash,
                'inventory.value': 0 if entry is None else entry.value(),
                'inventory.number': 0 if entry is None else entry.number,
                'inventory.price': 0 if entry is None else entry.price,
                'number': number,
                'action': action}
        self.test_data.append(data)

    def log(self, action: str, date: datetime, ticker: str, price: float, buy: bool, sell: bool) -> None:
        pass  # Do nothing
