from decimal import Decimal
from typing import Dict, NoReturn

from src.bo.broker_bo import BrokerBO
from src.bo.inventory_bo import InventoryBO
from src.dao.forward_dao import ForwardDAO


class ForwardBrokerBO(BrokerBO):

    def __init__(self, cash: Decimal, fee: Decimal, inventory: Dict[str, InventoryBO]) -> NoReturn:
        super().__init__(cash, fee, inventory)

    def buy(self, ticker: str, price: Decimal, number: Decimal) -> bool:
        success = super().buy(ticker, price, number)
        if success:
            ForwardDAO.create_buy(ticker, price, number, self._cash)
        return success

    def sell(self, ticker: str, price: Decimal, number: Decimal) -> bool:
        success = super().sell(ticker, price, number)
        if success:
            ForwardDAO.create_sell(ticker, price, number, self._cash)
        return success
