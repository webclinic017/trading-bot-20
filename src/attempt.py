from __future__ import annotations

from src.entity.evaluation_entity import EvaluationEntity


class Attempt:
    def __init__(self, amount_buy: float = 1000, distance_buy: float = 500, delta_buy: float = 1.5,
                 amount_sell: float = 1000, distance_sell: float = 500, delta_sell: float = 1.5) -> None:
        self.amount_buy: float = amount_buy
        self.distance_buy: float = distance_buy
        self.delta_buy: float = delta_buy
        self.amount_sell: float = amount_sell
        self.distance_sell: float = distance_sell
        self.delta_sell: float = delta_sell

    @classmethod
    def from_evaluation(cls, evaluation: EvaluationEntity) -> Attempt:
        return cls(evaluation.amountbuy, evaluation.distancebuy, evaluation.deltabuy,
                   evaluation.amountsell, evaluation.distancesell, evaluation.deltasell)
