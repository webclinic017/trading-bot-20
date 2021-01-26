from trading_bot import db
from trading_bot.bo.configuration_bo import ConfigurationBO
from trading_bot.bo.portfolio_bo import PortfolioBO


class Database:

    @staticmethod
    def init() -> None:
        db.create_all()
        ConfigurationBO.init()
        PortfolioBO.init()
