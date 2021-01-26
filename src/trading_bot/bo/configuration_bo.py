from decimal import Decimal
from typing import List

from trading_bot.dao.configuration_dao import ConfigurationDAO
from trading_bot.entity.configuration_entity import ConfigurationEntity
from trading_bot.enums.configuration_enum import ConfigurationEnum


class ConfigurationBO:

    @staticmethod
    def init() -> None:
        for configuration in ConfigurationEnum:
            ConfigurationDAO.create(configuration.identifier, configuration.val, configuration.description)

    @staticmethod
    def read_all() -> List[ConfigurationEntity]:
        return ConfigurationDAO.read_all()

    @staticmethod
    def read_filter_by_identifier(identifier: str) -> ConfigurationEntity:
        return ConfigurationDAO.read_filter_by_identifier(identifier)

    @staticmethod
    def update(identifier: str, value: Decimal) -> None:
        return ConfigurationDAO.update(identifier, value)
