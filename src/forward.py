from datetime import datetime
from typing import Dict, List, Tuple

from pandas import DataFrame

from src.action import Action
from src.analyser import Analyser
from src.attempt import Attempt
from src.broker import Broker
from src.constants import FEE, INITIAL_CASH
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dao.intraday_dao import IntradayDAO
from src.entity.evaluation_entity import EvaluationEntity
from src.entity.forward_entity import ForwardEntity
from src.entity.intraday_entity import IntradayEntity
from src.inventory import Inventory
from src.statistic import Statistic
from src.strategy import Strategy
from src.utils import Utils


class Forward:

    @staticmethod
    def start() -> None:
        latest_date: List[datetime] = ForwardDAO.read_latest_date()
        evaluation: EvaluationEntity = EvaluationDAO.read_order_by_sum()
        if evaluation is None or Utils.is_today(latest_date[0]) or not Utils.is_working_day_ny():
            return
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
        broker = Broker(INITIAL_CASH, FEE)
        for row in rows:
            if row.action == Action.BUY:
                broker.buy(row.ticker, row.price, row.number)
            elif row.action == Action.SELL:
                broker.sell(row.ticker, row.price, row.number)
        return broker.inventory, broker.cash

    @staticmethod
    def update(inventory: Dict[str, Inventory], cash: float) -> Tuple[Dict[str, Inventory], float, float]:
        total: float = 0
        total_value: float = 0
        for ticker, entry in inventory.items():
            intraday: IntradayEntity = IntradayDAO.read_filter_by_ticker_first(ticker)
            if intraday is None:
                continue
            entry.price = float(intraday.close)
            total_value += entry.value()
        total += cash + total_value
        return inventory, total_value, total


if __name__ == '__main__':
    Forward.start()
