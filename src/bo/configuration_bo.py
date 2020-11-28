from decimal import Decimal
from typing import NoReturn, List

from src.dao.configuration_dao import ConfigurationDAO
from src.entity.configuration_entity import ConfigurationEntity
from src.enums.configuration_enum import ConfigurationEnum


class ConfigurationBO:

    @staticmethod
    def init() -> NoReturn:
        for configuration in ConfigurationEnum:
            ConfigurationDAO.create(configuration.identifier, configuration.val, configuration.description)

    @staticmethod
    def read_all() -> List[ConfigurationEntity]:
        return ConfigurationDAO.read_all()

    @staticmethod
    def read_filter_by_identifier(identifier: str) -> ConfigurationEntity:
        return ConfigurationDAO.read_filter_by_identifier(identifier)

    @staticmethod
    def update(identifier: str, value: Decimal) -> NoReturn:
        return ConfigurationDAO.update(identifier, value)
