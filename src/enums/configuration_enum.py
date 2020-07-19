from enum import Enum


class ConfigurationEnum(Enum):
    FORWARD_CASH = ('FORWARD_CASH', 10000, 'Forward Cash')
    FORWARD_FEE = ('FORWARD_FEE', 3.9, 'Forward Fee')
    OPTIMIZE_CASH = ('OPTIMIZE_CASH', 10000, 'Optimizer Cash')
    OPTIMIZE_FEE = ('OPTIMIZE_FEE', 3.9, 'Optimizer Fee')

    def __init__(self, identifier, value, description):
        self.identifier = identifier
        self.v = value
        self.description = description
