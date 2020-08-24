import unittest

from src import db
from src.bo.configuration_bo import ConfigurationBO
from src.dao.configuration_dao import ConfigurationDAO
from src.entity.configuration_entity import ConfigurationEntity
from src.enums.configuration_enum import ConfigurationEnum
from tests.utils.utils import Utils


class ConfigurationBOTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    def setUp(self):
        Utils.truncate_tables()

    def test_create(self):
        ConfigurationBO.create()
        configurations = ConfigurationDAO.read_all()
        self.assertEqual(len(configurations), 4)
        for enum, configuration in zip(ConfigurationEnum.__iter__(), configurations):
            self.assertIsInstance(configuration, ConfigurationEntity)
            Utils.assert_attributes(configuration, identifier=enum.identifier, value=enum.val,
                                    description=enum.description)


if __name__ == '__main__':
    unittest.main()
