from typing import NoReturn

from src import db
from src.bo.configuration_bo import ConfigurationBO
from src.bo.portfolio_bo import PortfolioBO


class Database:

    @staticmethod
    def init() -> NoReturn:
        db.create_all()
        ConfigurationBO.init()
        PortfolioBO.init()
