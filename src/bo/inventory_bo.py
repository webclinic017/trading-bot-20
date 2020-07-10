class Inventory:

    def __init__(self, number: int, price: float) -> None:
        self.number = number
        self.price = price

    def value(self) -> float:
        return self.number * self.price
