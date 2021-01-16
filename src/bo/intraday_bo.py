from datetime import datetime
from decimal import Decimal
from operator import attrgetter
from time import sleep
from typing import List, Dict, Tuple, NoReturn

from flask import Request

from src import db
from src.common.constants import REQUEST_SLEEP
from src.dao.intraday_dao import IntradayDAO
from src.dao.stock_dao import StockDAO
from src.entity.intraday_entity import IntradayEntity
from src.utils.utils import Utils


class IntradayBO:

    @staticmethod
    def from_file(request: Request) -> NoReturn:
        IntradayDAO.create_from_file(request.files['file'].read())

    @staticmethod
    def to_file() -> List[Dict[str, str]]:
        rows: List[IntradayEntity] = IntradayDAO.read_order_by_date_asc()
        rows_dict: List[Dict[str, str]] = list(map(lambda row: dict(list(map(
            lambda i: (str(i[0]), str(float(i[1])) if isinstance(i[1], Decimal) else str(i[1])), filter(
                lambda e: not e[0].startswith('_'), row.__dict__.items())))), sorted(rows, key=attrgetter('ticker'))))
        return rows_dict

    @staticmethod
    def update(portfolio: Tuple[str, ...]) -> NoReturn:
        StockDAO.create_if_not_exists(portfolio)
        rows: List[IntradayEntity] = IntradayEntity.query.with_entities(IntradayEntity.ticker).filter(
            IntradayEntity.ticker.in_(portfolio)).distinct(IntradayEntity.ticker).all()
        if len(rows) < len(portfolio):
            tickers: List[str] = list(map(lambda r: r.ticker, rows))
            difference: str = Utils.first(sorted(list(set(portfolio) - set(tickers))))
            if difference is not None:
                IntradayDAO.create_ticker_extended(difference)
        else:
            for _ in range(24):
                rows: List[IntradayEntity] = db.session.query(IntradayEntity.ticker, db.func.max(
                    IntradayEntity.date)).group_by(IntradayEntity.ticker).all()
                if rows is not None:
                    latest_date: datetime = max(list(map(lambda r: r[1], rows)))
                    ticker: str = Utils.first(sorted(list(map(
                        lambda r: r.ticker, list(filter(lambda f: (f[1].date() != latest_date.date()), rows))))))
                    if ticker is not None:
                        IntradayDAO.create_ticker(ticker)
                if not Utils.is_test():
                    sleep(REQUEST_SLEEP)
