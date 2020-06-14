from src.analyser import Analyser
from src.attempt import Attempt
from src.broker import Broker
from src.constants import BUY, SELL, FEE, INITIAL_CASH
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dao.intraday_dao import IntradayDAO
from src.inventory import Inventory
from src.statistic import Statistic
from src.strategy import Strategy


class Forward:

    @staticmethod
    def start():
        evaluation = EvaluationDAO.read_order_by_sum()
        read_latest_date = IntradayDAO.read_latest_date()
        latest_date_dict = {r.ticker: r[0] for r in read_latest_date}
        rows = IntradayDAO.read_order_by_date_asc()
        frame = IntradayDAO.dataframe(rows)
        inventory, cash = Forward.init()
        broker = Broker(cash, FEE, ForwardDAO, inventory)
        statistic = Statistic('forward')
        attempt = Attempt.from_evaluation(evaluation)
        Analyser.analyse(frame, Strategy.counter_cyclical, broker, statistic, attempt, latest_date_dict)

    @staticmethod
    def init():
        rows = ForwardDAO.read()
        inventory = dict()
        cash = INITIAL_CASH
        for row in rows:
            entry = inventory.get(row.ticker, Inventory(0, row.price))
            total_price = row.price * row.number
            if row.action == BUY:
                entry.number += row.number
                cash = cash + total_price - FEE
            elif row.action == SELL:
                entry.number -= row.number
                cash = cash - total_price - FEE
            inventory[row.ticker] = entry
        return inventory, cash

    @staticmethod
    def update(inventory, cash):
        total = 0
        total_value = 0
        for ticker, entry in inventory.items():
            intraday = IntradayDAO.read_filter_by_ticker_first(ticker)
            entry.price = intraday.close
            total_value += entry.value()
        total += cash + total_value
        return inventory, total_value, total


if __name__ == '__main__':
    Forward.start()
