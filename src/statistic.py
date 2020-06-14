class Statistic:

    def __init__(self, name='statistic'):
        self.name = name
        self.test_data = []

    def plot(self, date, ticker, price, buy, sell):
        pass

    def test(self, action, number, ticker, broker):
        entry = broker.inventory.get(ticker)
        data = {'cash': broker.cash,
                'inventory.value': 0 if entry is None else entry.value(),
                'inventory.number': 0 if entry is None else entry.number,
                'inventory.price': 0 if entry is None else entry.price,
                'number': number,
                'action': action}
        self.test_data.append(data)

    def log(self, action, date, ticker, price, buy, sell):
        pass
