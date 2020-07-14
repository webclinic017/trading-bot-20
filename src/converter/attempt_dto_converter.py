from src.dto.attempt_dto import AttemptDTO
from src.entity.evaluation_entity import EvaluationEntity


class AttemptDTOConverter:

    @staticmethod
    def from_evaluation(evaluation: EvaluationEntity) -> AttemptDTO:
        return AttemptDTO(evaluation.amountbuy, evaluation.distancebuy, evaluation.deltabuy,
                          evaluation.amountsell, evaluation.distancesell, evaluation.deltasell)
