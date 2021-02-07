from decimal import Decimal
from typing import Dict

from trading_bot.bo.broker_bo import BrokerBO
from trading_bot.bo.inventory_bo import InventoryBO
from trading_bot.dao.forward_dao import ForwardDAO
from trading_bot.enums.strategy_enum import StrategyEnum


class ForwardBrokerBO(BrokerBO):

    def __init__(self, cash: Decimal, fee: Decimal, inventory: Dict[str, InventoryBO],
                 strategy: StrategyEnum) -> None:
        super().__init__(cash, fee, inventory)
        self.strategy = strategy

    def buy(self, symbol: str, price: Decimal, number: Decimal) -> bool:
        success = super().buy(symbol, price, number)
        if success:
            ForwardDAO.create_buy(symbol, price, number, self._cash, self.strategy)
        return success

    def sell(self, symbol: str, price: Decimal, number: Decimal) -> bool:
        success = super().sell(symbol, price, number)
        if success:
            ForwardDAO.create_sell(symbol, price, number, self._cash, self.strategy)
        return success
