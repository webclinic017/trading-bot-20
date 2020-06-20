import math
from typing import Dict, Type

from src.constants import INITIAL_CASH, FEE
from src.dao.broker_dao import BrokerDAO
from src.inventory import Inventory


class Broker:

    def __init__(self, cash: float = INITIAL_CASH, fee: float = FEE, dao: Type[BrokerDAO] = BrokerDAO,
                 inventory: Dict[str, Inventory] = None) -> None:
        self.dao: callable = dao
        self.cash: float = cash
        self.fee: float = fee
        self.inventory: Dict[str, Inventory] = dict() if inventory is None else inventory

    def update(self, ticker: str, price: float) -> None:
        if not math.isnan(price):
            entry: Inventory = self.inventory.get(ticker, Inventory(0, price))
            entry.price = price
            self.inventory[ticker] = entry

    def buy(self, ticker: str, price: float, number: int) -> bool:
        total_price: float = price * number
        if self.cash >= total_price:
            entry: Inventory = self.inventory.get(ticker, Inventory(0, price))
            entry.number += number
            entry.price = price
            self.inventory[ticker] = entry
            self.cash = self.cash - total_price - self.fee
            self.dao.create_buy(ticker, price, number, self.cash)
            return True
        return False

    def sell(self, ticker: str, price: float, number: int) -> bool:
        total_price: float = price * number
        entry: Inventory = self.inventory.get(ticker, Inventory(0, price))
        if entry.number >= number:
            entry.number -= number
            entry.price = price
            self.inventory[ticker] = entry
            self.cash = self.cash + total_price - self.fee
            self.dao.create_sell(ticker, price, number, self.cash)
            return True
        return False

    def funds(self) -> float:
        value: float = 0
        for ticker in self.inventory:
            value += self.inventory[ticker].value()
        return self.cash + value
