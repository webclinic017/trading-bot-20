from typing import List, Dict

from flask import Request

from src.dao.intraday_dao import IntradayDAO
from src.entity.intraday_entity import IntradayEntity


class IntradayBO:
    @staticmethod
    def from_file(request: Request) -> None:
        IntradayDAO.create_from_file(request.files['file'].read())

    @staticmethod
    def to_file() -> List[Dict[str, str]]:
        rows: List[IntradayEntity] = IntradayDAO.read_order_by_date_asc()
        rows_dict: List[Dict[str, str]] = list(
            map(lambda row: dict(filter(lambda e: not e[0].startswith('_'), row.__dict__.items())), rows))
        return rows_dict
