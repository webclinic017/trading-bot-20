class Inventory:

    def __init__(self, number, price):
        self.number = number
        self.price = price

    def value(self):
        return self.number * self.price
