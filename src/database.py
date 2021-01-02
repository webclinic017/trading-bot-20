from typing import NoReturn

from src.bo.configuration_bo import ConfigurationBO
from src.bo.portfolio_bo import PortfolioBO


class Database:

    @staticmethod
    def init() -> NoReturn:
        ConfigurationBO.init()
        PortfolioBO.init()
