class Attempt:
    def __init__(self, amount_buy=1000, distance_buy=500, delta_buy=1.5,
                 amount_sell=1000, distance_sell=500, delta_sell=1.5):
        self.amount_buy = amount_buy
        self.distance_buy = distance_buy
        self.delta_buy = delta_buy
        self.amount_sell = amount_sell
        self.distance_sell = distance_sell
        self.delta_sell = delta_sell

    @classmethod
    def from_evaluation(cls, evaluation):
        return cls(evaluation.amountbuy, evaluation.distancebuy, evaluation.deltabuy,
                   evaluation.amountsell, evaluation.distancesell, evaluation.deltasell)
