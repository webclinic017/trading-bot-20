import os
from csv import DictReader
from datetime import datetime
from decimal import Decimal
from typing import Final, Iterable

from pytz import timezone

from trading_bot import Utils
from trading_bot.common.constants import US_EASTERN
from trading_bot.dao.intraday_dao import IntradayDAO
from trading_bot.entity.intraday_entity import IntradayEntity


class IntradayUtils:
    YEAR_RANGE: Final[int] = 2
    MONTH_RANGE: Final[int] = 12
    CSV_PATH: Final[str] = os.path.join('..', '..', '..', 'data', 'symbol{}_year{}_month{}.csv')

    @classmethod
    def read_time_series_intraday_extended(cls, symbol: str = 'IBM') -> None:
        for year in range(cls.YEAR_RANGE):
            for month in range(cls.MONTH_RANGE):
                path: str = cls.CSV_PATH.format(symbol, year + 1, month + 1)
                IntradayUtils.from_csv(open(path, 'r'), symbol)

    @staticmethod
    def from_csv(csv_file: Iterable[str], symbol: str) -> None:
        reader: DictReader = DictReader(csv_file)
        for row in reader:
            intraday: IntradayEntity = IntradayEntity()
            Utils.set_attributes(intraday, date=timezone(US_EASTERN).localize(datetime.fromisoformat(row['time'])),
                                 open=Decimal(row['open']), high=Decimal(row['high']), low=Decimal(row['low']),
                                 close=Decimal(row['close']), volume=Decimal(row['volume']), symbol=symbol)
            IntradayDAO.persist(intraday)


if __name__ == '__main__':
    IntradayUtils.read_time_series_intraday_extended()
