import unittest

import pandas as pd

from src.dao.intraday_dao import IntradayDAO


class IntraDayDAOTestCase(unittest.TestCase):
    def test_init(self):
        data = {'date': ['2020-05-01 16:00:00', '2020-05-01 15:55:00'],
                '1. open': ['121.4000', '121.6703'],
                '2. high': ['121.8700', '121.8200'],
                '3. low': ['121.4000', '121.3900'],
                '4. close': ['121.8300', '121.3900'],
                '5. volume': ['219717', '119646']
                }
        frame = pd.DataFrame(data)
        for index, row in frame.iterrows():
            intraday = IntradayDAO.init(row, 'IBM')
            self.assertEqual(intraday.date, row['date'])
            self.assertEqual(intraday.open, row['1. open'])
            self.assertEqual(intraday.high, row['2. high'])
            self.assertEqual(intraday.low, row['3. low'])
            self.assertEqual(intraday.close, row['4. close'])
            self.assertEqual(intraday.volume, row['5. volume'])
            self.assertEqual(intraday.ticker, 'IBM')


if __name__ == '__main__':
    unittest.main()
