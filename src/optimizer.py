import copy
import math

from src.analyser import Analyser
from src.attempt import Attempt
from src.broker import Broker
from src.constants import INITIAL_CASH
from src.dao.evaluation_dao import EvaluationDAO
from src.dao.intraday_dao import IntradayDAO
from src.portfolio import Portfolio
from src.statistic import Statistic
from src.strategy import Strategy
from src.utils import Utils


# noinspection DuplicatedCode
class Optimizer:
    @staticmethod
    def optimise(tables):
        initial_cash = INITIAL_CASH

        evaluation = EvaluationDAO.read_order_by_sum()

        if evaluation is None:
            attempt = Attempt()
            optimise_sum = initial_cash * len(tables)
        else:
            attempt = Attempt.from_evaluation(evaluation)
            optimise_sum = float(evaluation.sum)

        while True:
            evaluation_attempt = copy.copy(attempt)
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

            evaluation = EvaluationDAO.read_attempt(evaluation_attempt)
            if evaluation is None:
                break

        evaluation_sum = 0
        analysis_funds = []
        table_number = len(tables)
        for i in range(table_number):
            analysis_number = i + 1
            statistic_name = 'statistic analysis{}'.format(analysis_number)
            statistic = Statistic(statistic_name)
            broker = Broker(initial_cash)
            Analyser.analyse(tables[i], Strategy.counter_cyclical, broker, statistic, evaluation_attempt)
            evaluation_sum += broker.funds()
            analysis_funds.append(broker.funds())
            if analysis_number == table_number and evaluation_sum > optimise_sum:
                EvaluationDAO.create(str(evaluation_sum), ','.join(map(str, analysis_funds)), evaluation_attempt)

    @staticmethod
    def main():
        portfolio = Portfolio.test_portfolio()
        number = 100
        group_number = 4
        group_size = int(number / group_number)
        groups = tuple(Utils.group(group_size, portfolio[:number]))
        while True:
            Optimizer.optimise(IntradayDAO.dataframe_group(groups))

    @staticmethod
    def start(portfolio, number, group_number):
        group_size = int(number / group_number)
        groups = tuple(Utils.group(group_size, portfolio[:number]))
        Optimizer.optimise(IntradayDAO.dataframe_group(groups))


if __name__ == '__main__':
    Optimizer.main()
