from src.dao.configuration_dao import ConfigurationDAO
from src.enums.configuration_enum import ConfigurationEnum


class ConfigurationBO:

    @staticmethod
    def create() -> None:
        for configuration in ConfigurationEnum:
            ConfigurationDAO.create(configuration.identifier, configuration.v, configuration.description)
