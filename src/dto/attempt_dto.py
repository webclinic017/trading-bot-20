from __future__ import annotations


class AttemptDTO:
    def __init__(self, amount_buy: int = 1000, distance_buy: int = 30, delta_buy: float = 1.5,
                 amount_sell: int = 1000, distance_sell: int = 30, delta_sell: float = 1.5) -> None:
        self.amount_buy: int = amount_buy
        self.distance_buy: int = distance_buy
        self.delta_buy: float = delta_buy
        self.amount_sell: int = amount_sell
        self.distance_sell: int = distance_sell
        self.delta_sell: float = delta_sell
