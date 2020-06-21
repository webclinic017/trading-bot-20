from typing import Dict, List, Tuple

from pandas import DataFrame

from src.analyser import Analyser
from src.attempt import Attempt
from src.broker import Broker
from src.constants import BUY, SELL, FEE, INITIAL_CASH
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dao.intraday_dao import IntradayDAO
from src.entity.evaluation_entity import EvaluationEntity
from src.entity.forward_entity import ForwardEntity
from src.entity.intraday_entity import IntradayEntity
from src.inventory import Inventory
from src.statistic import Statistic
from src.strategy import Strategy


class Forward:

    @staticmethod
    def start() -> None:
        evaluation: EvaluationEntity = EvaluationDAO.read_order_by_sum()
        read_latest_date: List[IntradayEntity] = IntradayDAO.read_latest_date()
        latest_date_dict: Dict[str, str] = {r.ticker: r[0] for r in read_latest_date}
        rows: List[IntradayEntity] = IntradayDAO.read_order_by_date_asc()
        frame: DataFrame = IntradayDAO.dataframe(rows)
        inventory, cash = Forward.init()
        broker: Broker = Broker(cash, FEE, ForwardDAO, inventory)
        statistic: Statistic = Statistic('forward')
        attempt: Attempt = Attempt.from_evaluation(evaluation)
        Analyser.analyse(frame, Strategy.counter_cyclical, broker, statistic, attempt, latest_date_dict)

    @staticmethod
    def init() -> Tuple[Dict[str, Inventory], float]:
        rows: List[ForwardEntity] = ForwardDAO.read()
        inventory: Dict[str, Inventory] = dict()
        cash: float = INITIAL_CASH
        for row in rows:
            entry: Inventory = inventory.get(row.ticker, Inventory(0, float(row.price)))
            total_price: float = float(row.price) * int(row.number)
            if row.action == BUY:
                entry.number += int(row.number)
                cash = cash + total_price - FEE
            elif row.action == SELL:
                entry.number -= int(row.number)
                cash = cash - total_price - FEE
            inventory[row.ticker] = entry
        return inventory, cash

    @staticmethod
    def update(inventory: Dict[str, Inventory], cash: float) -> Tuple[Dict[str, Inventory], float, float]:
        total: float = 0
        total_value: float = 0
        for ticker, entry in inventory.items():
            intraday: IntradayEntity = IntradayDAO.read_filter_by_ticker_first(ticker)
            entry.price = float(intraday.close)
            total_value += entry.value()
        total += cash + total_value
        return inventory, total_value, total


if __name__ == '__main__':
    Forward.start()
