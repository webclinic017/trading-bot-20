import math
from decimal import Decimal
from typing import Dict

from trading_bot.bo.inventory_bo import InventoryBO
from trading_bot.common.constants import ZERO


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

    def update(self, symbol: str, price: Decimal) -> None:
        if not math.isnan(price):
            entry: InventoryBO = self.__inventory.get(symbol, InventoryBO(ZERO, price))
            entry.price = price
            self.__inventory[symbol] = entry

    def buy(self, symbol: str, price: Decimal, number: Decimal) -> bool:
        total_price: Decimal = price * number  # TODO fee fehlt
        if self._cash >= total_price and number > 0:
            entry: InventoryBO = self.__inventory.get(symbol, InventoryBO(ZERO, price))
            entry.number += number
            entry.price = price
            self.__inventory[symbol] = entry
            self._cash = self._cash - total_price - self.__fee
            return True
        return False

    def sell(self, symbol: str, price: Decimal, number: Decimal) -> bool:
        total_price: Decimal = price * number  # TODO fee fehlt
        entry: InventoryBO = self.__inventory.get(symbol, InventoryBO(ZERO, price))
        if entry.number >= number > 0:
            entry.number -= number
            entry.price = price
            self.__inventory[symbol] = entry
            self._cash = self._cash + total_price - self.__fee
            return True
        return False

    def funds(self) -> Decimal:
        value: Decimal = ZERO
        for symbol in self.__inventory:
            value += self.__inventory[symbol].value()
        return self._cash + value
