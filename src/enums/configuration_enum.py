from decimal import Decimal
from enum import Enum


class ConfigurationEnum(Enum):
    FORWARD_CASH = ('FORWARD_CASH', Decimal('10000'), 'Forward Cash')
    FORWARD_FEE = ('FORWARD_FEE', Decimal('3.9'), 'Forward Fee')
    OPTIMIZE_CASH = ('OPTIMIZE_CASH', Decimal('10000'), 'Optimizer Cash')
    OPTIMIZE_FEE = ('OPTIMIZE_FEE', Decimal('3.9'), 'Optimizer Fee')

    def __init__(self, identifier: str, value: Decimal, description: str):
        self.identifier = identifier
        self.val = value
        self.description = description
