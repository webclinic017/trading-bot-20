from typing import List

from src.dao.dao import DAO
from src.dto.attempt_dto import AttemptDTO
from src.entity.evaluation_entity import EvaluationEntity
from src.utils.utils import Utils


class EvaluationDAO:
    @staticmethod
    def create(s: float, funds: str, attempt: AttemptDTO) -> None:
        evaluation: EvaluationEntity = EvaluationEntity()
        evaluation.timestamp = Utils.now()
        evaluation.sum = str(s)
        evaluation.funds = funds
        Utils.set_attributes(evaluation, amount_buy=str(attempt.amount_buy), distance_buy=str(attempt.distance_buy),
                             delta_buy=str(attempt.delta_buy), amount_sell=str(attempt.amount_sell),
                             distance_sell=str(attempt.distance_sell), delta_sell=str(attempt.delta_sell))
        DAO.persist(evaluation)

    @staticmethod
    def read_order_by_sum() -> EvaluationEntity:
        return EvaluationEntity.query.order_by(EvaluationEntity.sum.desc()).first()

    @staticmethod
    def read_attempt(attempt: AttemptDTO) -> EvaluationEntity:
        return EvaluationEntity.query.filter_by(
            amount_buy=attempt.amount_buy).filter_by(
            distance_buy=attempt.distance_buy).filter_by(
            delta_buy=attempt.delta_buy).filter_by(
            amount_sell=attempt.amount_sell).filter_by(
            distance_sell=attempt.distance_sell).filter_by(
            delta_sell=attempt.delta_sell).first()

    @staticmethod
    def read_all() -> List[EvaluationEntity]:
        return EvaluationEntity.query.all()
