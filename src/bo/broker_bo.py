import math
from decimal import Decimal
from typing import Dict

from src.bo.inventory_bo import InventoryBO


class BrokerBO:

    def __init__(self, cash: Decimal, fee: Decimal, inventory: Dict[str, InventoryBO] = None) -> None:
        self._cash: Decimal = cash
        self.__fee: Decimal = fee
        self.__inventory: Dict[str, InventoryBO] = dict() if inventory is None else inventory

    @property
    def cash(self):
        return self._cash

    @property
    def inventory(self):
        return self.__inventory

    def update(self, ticker: str, price: Decimal) -> None:
        if not math.isnan(price):
            entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(Decimal('0'), price))
            entry.price = price
            self.__inventory[ticker] = entry

    def buy(self, ticker: str, price: Decimal, number: Decimal) -> bool:
        total_price: Decimal = price * number
        if self._cash >= total_price:
            entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(Decimal('0'), price))
            entry.number += number
            entry.price = price
            self.__inventory[ticker] = entry
            self._cash = self._cash - total_price - self.__fee
            return True
        return False

    def sell(self, ticker: str, price: Decimal, number: Decimal) -> bool:
        total_price: Decimal = price * number
        entry: InventoryBO = self.__inventory.get(ticker, InventoryBO(Decimal('0'), price))
        if entry.number >= number:
            entry.number -= number
            entry.price = price
            self.__inventory[ticker] = entry
            self._cash = self._cash + total_price - self.__fee
            return True
        return False

    def funds(self) -> Decimal:
        value: Decimal = Decimal('0')
        for ticker in self.__inventory:
            value += self.__inventory[ticker].value()
        return self._cash + value
