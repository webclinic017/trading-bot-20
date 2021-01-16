import math
from decimal import Decimal
from typing import Dict, NoReturn

from src.bo.inventory_bo import InventoryBO
from src.common.constants import ZERO


class BrokerBO:

    def __init__(self, cash: Decimal, fee: Decimal, inventory: Dict[str, InventoryBO] = None) -> NoReturn:
        self._cash: Decimal = cash
        self.__fee: Decimal = fee
        self.__inventory: Dict[str, InventoryBO] = dict() if inventory is None else inventory

    @property
    def cash(self):
        return self._cash

    @property
    def inventory(self):
        return self.__inventory

    def update(self, ticker: str, price: Decimal) -> NoReturn:
        if not math.isnan(price):
            entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(ZERO, price))
            entry.price = price
            self.__inventory[ticker] = entry

    def buy(self, ticker: str, price: Decimal, number: Decimal) -> bool:
        total_price: Decimal = price * number
        if self._cash >= total_price and number > 0:
            entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(ZERO, price))
            entry.number += number
            entry.price = price
            self.__inventory[ticker] = entry
            self._cash = self._cash - total_price - self.__fee
            return True
        return False

    def sell(self, ticker: str, price: Decimal, number: Decimal) -> bool:
        total_price: Decimal = price * number
        entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(ZERO, price))
        if entry.number >= number > 0:
            entry.number -= number
            entry.price = price
            self.__inventory[ticker] = entry
            self._cash = self._cash + total_price - self.__fee
            return True
        return False

    def funds(self) -> Decimal:
        value: Decimal = ZERO
        for ticker in self.__inventory:
            value += self.__inventory[ticker].value()
        return self._cash + value
