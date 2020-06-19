import re

import requests


class Isin:
    @staticmethod
    def isin(ticker: str) -> str:
        url = 'https://markets.businessinsider.com/ajax/' \
              'SearchController_Suggest?max_results=25&query=%s' \
              % ticker
        data = requests.get(url=url).text

        match = re.search('([A-Z]{2})([A-Z0-9]{9})([0-9])', data)
        return match.group(0)
