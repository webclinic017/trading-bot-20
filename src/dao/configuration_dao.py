from decimal import Decimal
from typing import List, NoReturn

from src.dao.base_dao import BaseDAO
from src.entity.configuration_entity import ConfigurationEntity
from src.utils.utils import Utils


class ConfigurationDAO(BaseDAO):

    @classmethod
    def create(cls, identifier: str, value: str, description: str) -> NoReturn:
        configuration: ConfigurationEntity = ConfigurationEntity()
        Utils.set_attributes(configuration, identifier=identifier, value=value, description=description)
        cls.persist(configuration)

    @staticmethod
    def read_all() -> List[ConfigurationEntity]:
        return ConfigurationEntity.query.order_by(ConfigurationEntity.identifier.asc()).all()

    @staticmethod
    def read_filter_by_identifier(identifier: str) -> ConfigurationEntity:
        return ConfigurationEntity.query.filter_by(identifier=identifier).first()

    @classmethod
    def update(cls, identifier: str, value: Decimal) -> NoReturn:
        configuration = cls.read_filter_by_identifier(identifier)
        configuration.value = value
        cls.commit()
