from random import choice
from typing import List, Optional, Final, Any

from pandas import DataFrame
from predictor.dto.prediction_dto import PredictionDTO
from predictor.main import Main
from predictor.utils.predictor_utils import PredictorUtils

from trading_bot.converter.intraday_entity_converter import IntradayEntityConverter
from trading_bot.dao.intraday_dao import IntradayDAO
from trading_bot.entity.intraday_entity import IntradayEntity


class PredictorAdapter:
    STEP: Final[int] = 1

    @classmethod
    def fit(cls, **kwargs: Any) -> None:
        sufficient_data: int = PredictorUtils.SUFFICIENT_DATA
        if 'sufficient_data' in kwargs:
            sufficient_data = kwargs['sufficient_data']
        portfolio: List[str] = [i[0] for i in IntradayDAO.read_having_sufficient_data(sufficient_data)]
        intraday_list: List[IntradayEntity] = IntradayDAO.read_filter_by_symbol(choice(portfolio))
        if len(intraday_list) >= sufficient_data:
            Main.fit(IntradayEntityConverter.to_float_dataframe(intraday_list), step=cls.STEP, show_visualization=False,
                     **kwargs)

    @classmethod
    def predict(cls, frame: DataFrame, **kwargs: Any) -> Optional[PredictionDTO]:
        past: int = kwargs['past'] if 'past' in kwargs else PredictorUtils.PAST
        if len(frame) >= past:
            return Main.predict(frame, step=cls.STEP, show_visualization=False, **kwargs)
