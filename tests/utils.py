import copy
import math

import numpy as np
import pandas as pd
from pandas import DataFrame


class Utils:
    @staticmethod
    def create_frame() -> DataFrame:
        dates = pd.date_range('1/1/2000', periods=150)
        prices_aaa = np.full((150, 1), float(500))
        prices_bbb = copy.copy(prices_aaa)
        prices_aaa[30:60] = prices_aaa[90:120] = float(100)
        prices_bbb[0:30] = math.nan
        tickers = ['AAA', 'BBB']
        prices = np.hstack((prices_aaa, prices_bbb))
        frame = DataFrame(prices, index=dates, columns=tickers)
        frame.sort_index(inplace=True, ascending=True)
        return frame
