import copy
import math
from typing import Tuple, List

from pandas import DataFrame

from src.analyser import Analyser
from src.attempt import Attempt
from src.broker import Broker
from src.constants import INITIAL_CASH
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.intraday_dao import IntradayDAO
from src.entity.evaluation_entity import EvaluationEntity
from src.portfolio import Portfolio
from src.statistic import Statistic
from src.strategy import Strategy
from src.utils import Utils


# noinspection DuplicatedCode
class Optimizer:
    @staticmethod
    def optimise(tables: List[DataFrame]) -> None:
        initial_cash: float = INITIAL_CASH

        evaluation: EvaluationEntity = EvaluationDAO.read_order_by_sum()

        if evaluation is None:
            attempt: Attempt = Attempt()
            optimise_sum: float = initial_cash * len(tables)
        else:
            attempt: Attempt = Attempt.from_evaluation(evaluation)
            optimise_sum: float = float(evaluation.sum)

        while True:
            evaluation_attempt: Attempt = copy.copy(attempt)
            evaluation_attempt.amount_buy += int(attempt.amount_buy * Utils.inverse()) * Utils.negation()
            evaluation_attempt.distance_buy += int(attempt.distance_buy * Utils.inverse()) * Utils.negation()
            evaluation_attempt.delta_buy += attempt.delta_buy * Utils.inverse() * Utils.negation()

            evaluation_attempt.amount_sell += int(attempt.amount_sell * Utils.inverse()) * Utils.negation()
            evaluation_attempt.distance_sell += int(attempt.distance_sell * Utils.inverse()) * Utils.negation()
            evaluation_attempt.delta_sell += attempt.delta_sell * Utils.inverse() * Utils.negation()

            if not Utils.valid(0, evaluation_attempt.amount_buy, math.inf) \
                    or not Utils.valid(0, evaluation_attempt.distance_buy, math.inf) \
                    or not Utils.valid(0, evaluation_attempt.delta_buy, math.inf) \
                    or not Utils.valid(0, evaluation_attempt.amount_sell, math.inf) \
                    or not Utils.valid(0, evaluation_attempt.distance_sell, math.inf) \
                    or not Utils.valid(0, evaluation_attempt.delta_sell, math.inf):
                continue

            evaluation: EvaluationEntity = EvaluationDAO.read_attempt(evaluation_attempt)
            if evaluation is None:
                break

        evaluation_sum: float = 0
        analysis_funds: List[float] = []
        table_number: int = len(tables)
        for i in range(table_number):
            analysis_number: int = i + 1
            statistic_name: str = 'statistic analysis{}'.format(analysis_number)
            statistic: Statistic = Statistic(statistic_name)
            broker: Broker = Broker(initial_cash)
            Analyser.analyse(tables[i], Strategy.counter_cyclical, broker, statistic, evaluation_attempt)
            evaluation_sum += broker.funds()
            analysis_funds.append(broker.funds())
            if analysis_number == table_number and evaluation_sum > optimise_sum:
                EvaluationDAO.create(evaluation_sum, ','.join(map(str, analysis_funds)), evaluation_attempt)

    @staticmethod
    def main() -> None:
        portfolio: List[str] = Portfolio.test_portfolio()
        number: int = 100
        group_number: int = 4
        group_size: int = int(number / group_number)
        groups: Tuple[Tuple[str]] = Utils.group(group_size, portfolio[:number])
        while True:
            Optimizer.optimise(IntradayDAO.dataframe_group(groups))

    @staticmethod
    def start(portfolio: List[str], number: int, group_number: int) -> None:
        group_size: int = int(number / group_number)
        groups: Tuple[Tuple[str]] = Utils.group(group_size, portfolio[:number])
        Optimizer.optimise(IntradayDAO.dataframe_group(groups))


if __name__ == '__main__':
    Optimizer.main()
