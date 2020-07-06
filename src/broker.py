import math
from typing import Dict, Type

from src.constants import INITIAL_CASH, FEE
from src.dao.broker_dao import BrokerDAO
from src.inventory import Inventory


class Broker:

    def __init__(self, cash: float = INITIAL_CASH, fee: float = FEE, dao: Type[BrokerDAO] = BrokerDAO,
                 inventory: Dict[str, Inventory] = None) -> None:
        self.__dao: callable = dao
        self.__cash: float = cash
        self.__fee: float = fee
        self.__inventory: Dict[str, Inventory] = dict() if inventory is None else inventory

    @property
    def cash(self):
        return self.__cash

    @property
    def inventory(self):
        return self.__inventory

    def update(self, ticker: str, price: float) -> None:
        if not math.isnan(price):
            entry: Inventory = self.__inventory.get(ticker, Inventory(0, price))
            entry.price = price
            self.__inventory[ticker] = entry

    def buy(self, ticker: str, price: float, number: int) -> bool:
        total_price: float = price * number
        if self.__cash >= total_price:
            entry: Inventory = self.__inventory.get(ticker, Inventory(0, price))
            entry.number += number
            entry.price = price
            self.__inventory[ticker] = entry
            self.__cash = self.__cash - total_price - self.__fee
            self.__dao.create_buy(ticker, price, number, self.__cash)
            return True
        return False

    def sell(self, ticker: str, price: float, number: int) -> bool:
        total_price: float = price * number
        entry: Inventory = self.__inventory.get(ticker, Inventory(0, price))
        if entry.number >= number:
            entry.number -= number
            entry.price = price
            self.__inventory[ticker] = entry
            self.__cash = self.__cash + total_price - self.__fee
            self.__dao.create_sell(ticker, price, number, self.__cash)
            return True
        return False

    def funds(self) -> float:
        value: float = 0
        for ticker in self.__inventory:
            value += self.__inventory[ticker].value()
        return self.__cash + value
