from decimal import Decimal

from tests.base_test_case import BaseTestCase
from trading_bot import db
from trading_bot.bo.configuration_bo import ConfigurationBO
from trading_bot.dao.configuration_dao import ConfigurationDAO
from trading_bot.entity.configuration_entity import ConfigurationEntity
from trading_bot.enums.configuration_enum import ConfigurationEnum


class ConfigurationDAOTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()
        ConfigurationBO.init()

    def test_read_filter_by_identifier(self):
        configuration = ConfigurationDAO.read_filter_by_identifier(ConfigurationEnum.FORWARD_CASH.identifier)
        self.assertIsInstance(configuration, ConfigurationEntity)
        self.assert_attributes(configuration, identifier=ConfigurationEnum.FORWARD_CASH.identifier,
                               value=ConfigurationEnum.FORWARD_CASH.val,
                               description=ConfigurationEnum.FORWARD_CASH.description)

    def test_update(self):
        ConfigurationDAO.update(ConfigurationEnum.FORWARD_CASH.identifier, Decimal('10001'))
        configuration = ConfigurationDAO.read_filter_by_identifier(ConfigurationEnum.FORWARD_CASH.identifier)
        self.assertIsInstance(configuration, ConfigurationEntity)
        self.assert_attributes(configuration, identifier=ConfigurationEnum.FORWARD_CASH.identifier,
                               value=10001, description=ConfigurationEnum.FORWARD_CASH.description)
