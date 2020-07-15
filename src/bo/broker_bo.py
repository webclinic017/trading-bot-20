import math
from typing import Dict

from src.bo.inventory_bo import InventoryBO
from src.constants import INITIAL_CASH, FEE


class BrokerBO:

    def __init__(self, cash: float = INITIAL_CASH, fee: float = FEE, inventory: Dict[str, InventoryBO] = None) -> None:
        self._cash: float = cash
        self.__fee: float = fee
        self.__inventory: Dict[str, InventoryBO] = dict() if inventory is None else inventory

    @property
    def cash(self):
        return self._cash

    @property
    def inventory(self):
        return self.__inventory

    def update(self, ticker: str, price: float) -> None:
        if not math.isnan(price):
            entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(0, price))
            entry.price = price
            self.__inventory[ticker] = entry

    def buy(self, ticker: str, price: float, number: int) -> bool:
        total_price: float = price * number
        if self._cash >= total_price:
            entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(0, price))
            entry.number += number
            entry.price = price
            self.__inventory[ticker] = entry
            self._cash = self._cash - total_price - self.__fee
            return True
        return False

    def sell(self, ticker: str, price: float, number: int) -> bool:
        total_price: float = price * number
        entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(0, price))
        if entry.number >= number:
            entry.number -= number
            entry.price = price
            self.__inventory[ticker] = entry
            self._cash = self._cash + total_price - self.__fee
            return True
        return False

    def funds(self) -> float:
        value: float = 0
        for ticker in self.__inventory:
            value += self.__inventory[ticker].value()
        return self._cash + value
