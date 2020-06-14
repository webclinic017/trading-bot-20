import math

from src.constants import INITIAL_CASH, FEE
from src.dao.broker_dao import BrokerDAO
from src.inventory import Inventory


class Broker:

    def __init__(self, cash=INITIAL_CASH, fee=FEE, dao=BrokerDAO, inventory=None):
        self.dao = dao
        self.cash = cash
        self.fee = fee
        self.inventory = dict() if inventory is None else inventory

    def update(self, ticker, price):
        if not math.isnan(price):
            entry = self.inventory.get(ticker, Inventory(0, price))
            entry.price = price
            self.inventory[ticker] = entry

    def buy(self, ticker, price, number):
        total_price = price * number
        if self.cash >= total_price:
            entry = self.inventory.get(ticker, Inventory(0, price))
            entry.number += number
            entry.price = price
            self.inventory[ticker] = entry
            self.cash = self.cash - total_price - self.fee
            self.dao.create_buy(ticker, price, number, self.cash)
            return True
        return False

    def sell(self, ticker, price, number):
        total_price = price * number
        entry = self.inventory.get(ticker, Inventory(0, price))
        if entry.number >= number:
            entry.number -= number
            entry.price = price
            self.inventory[ticker] = entry
            self.cash = self.cash + total_price - self.fee
            self.dao.create_sell(ticker, price, number, self.cash)
            return True
        return False

    def funds(self):
        value = 0
        for ticker in self.inventory:
            value += self.inventory[ticker].value()
        return self.cash + value
