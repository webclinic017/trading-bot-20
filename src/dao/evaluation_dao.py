from typing import List

from src.attempt import Attempt
from src.dao.dao import DAO
from src.entity.evaluation_entity import EvaluationEntity


class EvaluationDAO:
    @staticmethod
    def create(s: float, funds: str, attempt: Attempt) -> None:
        evaluation: EvaluationEntity = EvaluationEntity()
        evaluation.sum = str(s)
        evaluation.funds = funds
        evaluation.amountbuy = str(attempt.amount_buy)
        evaluation.distancebuy = str(attempt.distance_buy)
        evaluation.deltabuy = str(attempt.delta_buy)
        evaluation.amountsell = str(attempt.amount_sell)
        evaluation.distancesell = str(attempt.distance_sell)
        evaluation.deltasell = str(attempt.delta_sell)
        DAO.persist(evaluation)

    @staticmethod
    def read_order_by_sum() -> EvaluationEntity:
        return EvaluationEntity.query.order_by(EvaluationEntity.sum.desc()).first()

    @staticmethod
    def read_attempt(attempt: Attempt) -> EvaluationEntity:
        return EvaluationEntity.query. \
            filter_by(amountbuy=attempt.amount_buy). \
            filter_by(distancebuy=attempt.distance_buy). \
            filter_by(deltabuy=attempt.delta_buy). \
            filter_by(amountsell=attempt.amount_sell). \
            filter_by(distancesell=attempt.distance_sell). \
            filter_by(deltasell=attempt.delta_sell).first()

    @staticmethod
    def read_all() -> List[EvaluationEntity]:
        return EvaluationEntity.query.all()
