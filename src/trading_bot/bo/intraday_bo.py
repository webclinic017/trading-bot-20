from datetime import datetime
from time import sleep
from typing import List, Callable, Dict, Tuple

from pandas import DataFrame

from trading_bot import db
from trading_bot.common.constants import REQUEST_SLEEP
from trading_bot.converter.intraday_entity_converter import IntradayEntityConverter
from trading_bot.dao.intraday_dao import IntradayDAO
from trading_bot.dao.stock_dao import StockDAO
from trading_bot.entity.intraday_entity import IntradayEntity
from trading_bot.utils.utils import Utils


class IntradayBO:

    @staticmethod
    def sort_by_date(intraday_list: List[IntradayEntity]) -> List[IntradayEntity]:
        return sorted(intraday_list, key=lambda i: i.date)

    @staticmethod
    def group_by_symbol(intraday_list: List[IntradayEntity]) -> Dict[str, List[IntradayEntity]]:
        return {b: [a for a in intraday_list if a.symbol == b] for b in set(map(lambda b: b.symbol, intraday_list))}

    @staticmethod
    def update(backward_forward_portfolio: Callable[[], List[str]]) -> None:
        portfolio: List[str] = backward_forward_portfolio()
        StockDAO.create_if_not_exists(portfolio)
        rows: List[IntradayEntity] = IntradayEntity.query.with_entities(IntradayEntity.symbol).filter(
            IntradayEntity.symbol.in_(portfolio)).distinct(IntradayEntity.symbol).all()
        if len(rows) < len(portfolio):
            symbols: List[str] = list(map(lambda r: r.symbol, rows))
            difference: str = Utils.first(sorted(list(set(portfolio) - set(symbols))))
            if difference is not None:
                IntradayDAO.create_symbol_extended(difference)
        else:
            for _ in range(24):
                rows: List[IntradayEntity] = db.session.query(IntradayEntity.symbol, db.func.max(
                    IntradayEntity.date)).group_by(IntradayEntity.symbol).all()
                if rows is not None and len(rows) > 0:
                    latest_date: datetime = max(list(map(lambda r: r[1], rows))).date()
                    symbol: str = Utils.first(sorted(list(map(
                        lambda r: r.symbol, list(filter(lambda f, d=latest_date: (f[1].date() != d), rows))))))
                    if symbol is not None:
                        IntradayDAO.create_symbol(symbol)
                if not Utils.is_test():
                    sleep(REQUEST_SLEEP)

    @staticmethod
    def intraday_list_group(group: Tuple[Tuple[str]]) -> List[Dict[str, DataFrame]]:
        return list(map(lambda g: {s: IntradayEntityConverter.to_float_dataframe(
            IntradayDAO.read_filter_by_symbol_order_by_date_limit(s)) for s in g}, group))

    @staticmethod
    def intraday_list(portfolio: List[str]) -> Dict[str, DataFrame]:
        return {i: IntradayEntityConverter.to_float_dataframe(
            IntradayDAO.read_filter_by_symbol_order_by_date(i)) for i in portfolio}
