import random


class Utils:
    @staticmethod
    def valid(start, value, stop):
        return start <= value <= stop

    @staticmethod
    def negation():
        return 1 if random.random() < 0.5 else -1

    @staticmethod
    def inverse():
        return random.random() if random.random() < 0.5 else 1 / random.random()

    @staticmethod
    def group(n, iterable):
        args = [iter(iterable)] * n
        return zip(*args)
