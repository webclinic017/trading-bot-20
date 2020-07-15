from typing import Dict

from src.bo.broker_bo import BrokerBO
from src.bo.inventory_bo import InventoryBO
from src.dao.forward_dao import ForwardDAO


class ForwardBrokerBO(BrokerBO):

    def __init__(self, cash: float, fee: float, inventory: Dict[str, InventoryBO]) -> None:
        super().__init__(cash, fee, inventory)

    def buy(self, ticker: str, price: float, number: int) -> bool:
        success = super().buy(ticker, price, number)
        if success:
            ForwardDAO.create_buy(ticker, price, number, self._cash)
        return success

    def sell(self, ticker: str, price: float, number: int) -> bool:
        success = super().sell(ticker, price, number)
        if success:
            ForwardDAO.create_sell(ticker, price, number, self._cash)
        return success
