from decimal import Decimal
from typing import List, NoReturn

from src.dao.dao import DAO
from src.entity.configuration_entity import ConfigurationEntity
from src.utils.utils import Utils


class ConfigurationDAO:

    @staticmethod
    def create(identifier: str, value: str, description: str) -> NoReturn:
        configuration: ConfigurationEntity = ConfigurationEntity()
        Utils.set_attributes(configuration, identifier=identifier, value=value, description=description)
        DAO.persist(configuration)

    @staticmethod
    def read_all() -> List[ConfigurationEntity]:
        return ConfigurationEntity.query.order_by(ConfigurationEntity.identifier.asc()).all()

    @staticmethod
    def read_filter_by_identifier(identifier: str) -> ConfigurationEntity:
        return ConfigurationEntity.query.filter_by(identifier=identifier).first()

    @staticmethod
    def update(identifier: str, value: Decimal) -> NoReturn:
        configuration = ConfigurationDAO.read_filter_by_identifier(identifier)
        configuration.value = value
        DAO.commit()
