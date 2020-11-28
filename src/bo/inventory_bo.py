from decimal import Decimal
from typing import NoReturn


class InventoryBO:

    def __init__(self, number: Decimal, price: Decimal) -> NoReturn:
        self.number = number
        self.price = price

    def value(self) -> Decimal:
        return self.number * self.price
