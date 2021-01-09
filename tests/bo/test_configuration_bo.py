from decimal import Decimal

from src import db
from src.bo.configuration_bo import ConfigurationBO
from src.entity.configuration_entity import ConfigurationEntity
from src.enums.configuration_enum import ConfigurationEnum
from tests.base_test_case import BaseTestCase


class ConfigurationBOTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        self.truncate_tables()

    def test_init(self):
        ConfigurationBO.init()
        configurations = ConfigurationBO.read_all()
        self.assertEqual(len(configurations), 4)
        for enum, configuration in zip(ConfigurationEnum.__iter__(), configurations):
            self.assertIsInstance(configuration, ConfigurationEntity)
            self.assert_attributes(configuration, identifier=enum.identifier, value=enum.val,
                                   description=enum.description)

    def test_read_filter_by_identifier(self):
        ConfigurationBO.init()
        configuration = ConfigurationBO.read_filter_by_identifier('FORWARD_CASH')
        self.assertIsInstance(configuration, ConfigurationEntity)
        self.assert_attributes(configuration, identifier='FORWARD_CASH', value=Decimal('10000'),
                               description='Forward Cash')
