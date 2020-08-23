from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Tuple

from pandas import DataFrame

from src.bo.analyser_bo import AnalyserBO
from src.bo.broker_bo import BrokerBO
from src.bo.forward_broker_bo import ForwardBrokerBO
from src.bo.inventory_bo import InventoryBO
from src.bo.statistic_bo import StatisticBO
from src.bo.strategy_bo import StrategyBO
from src.constants import ZERO
from src.converter.attempt_dto_converter import AttemptDTOConverter
from src.dao.configuration_dao import ConfigurationDAO
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.forward_dao import ForwardDAO
from src.dao.intraday_dao import IntradayDAO
from src.dto.attempt_dto import AttemptDTO
from src.entity.evaluation_entity import EvaluationEntity
from src.entity.forward_entity import ForwardEntity
from src.entity.intraday_entity import IntradayEntity
from src.enums.action_enum import ActionEnum
from src.enums.configuration_enum import ConfigurationEnum
from src.utils.utils import Utils


class ForwardBO:

    @staticmethod
    def start() -> None:
        latest_date: datetime = ForwardDAO.read_latest_date()
        evaluation: EvaluationEntity = EvaluationDAO.read_order_by_sum()
        if evaluation is None or Utils.is_today(latest_date) or not Utils.is_working_day_ny():
            return
        read_latest_date: List[IntradayEntity] = IntradayDAO.read_latest_date()
        latest_date_dict: Dict[str, str] = {r.ticker: r[0] for r in read_latest_date}
        rows: List[IntradayEntity] = IntradayDAO.read_order_by_date_asc()
        frame: DataFrame = IntradayDAO.dataframe(rows)
        inventory, cash, fee = ForwardBO.init()
        broker: BrokerBO = ForwardBrokerBO(cash, fee, inventory)
        statistic: StatisticBO = StatisticBO('forward')
        attempt: AttemptDTO = AttemptDTOConverter.from_evaluation(evaluation)
        AnalyserBO.analyse(frame, StrategyBO.counter_cyclical, broker, statistic, attempt, latest_date_dict)

    @staticmethod
    def init() -> Tuple[Dict[str, InventoryBO], Decimal, Decimal]:
        cash: Decimal = ConfigurationDAO.read_filter_by_identifier(ConfigurationEnum.FORWARD_CASH.identifier).value
        fee: Decimal = ConfigurationDAO.read_filter_by_identifier(ConfigurationEnum.OPTIMIZE_FEE.identifier).value
        rows: List[ForwardEntity] = ForwardDAO.read()
        broker = BrokerBO(cash, fee)
        for row in rows:
            if row.action == ActionEnum.BUY:
                broker.buy(row.ticker, row.price, row.number)
            elif row.action == ActionEnum.SELL:
                broker.sell(row.ticker, row.price, row.number)
        return broker.inventory, broker.cash, fee

    @staticmethod
    def update(inventory: Dict[str, InventoryBO], cash: Decimal) -> Tuple[Dict[str, InventoryBO], Decimal, Decimal]:
        total: Decimal = ZERO
        total_value: Decimal = ZERO
        for ticker, entry in inventory.items():
            intraday: IntradayEntity = IntradayDAO.read_filter_by_ticker_first(ticker)
            if intraday is None:
                continue
            entry.price = Decimal(intraday.close)
            total_value += entry.value()
        total += cash + total_value
        return inventory, total_value, total


if __name__ == '__main__':
    ForwardBO.start()
