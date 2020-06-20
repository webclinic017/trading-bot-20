import hashlib
import json
import re
from typing import List, Tuple, Dict, Any

import lxml.html as lh
import requests
from fake_useragent import UserAgent
from requests import Response
from yahoo_fin.stock_info import tickers_sp500


class Portfolio:

    @staticmethod
    def test_portfolio(size: int = 100) -> List[str]:
        return sorted(tickers_sp500(), key=lambda x: hashlib.md5(x.encode()).hexdigest())[:size]

    @staticmethod
    def prod_portfolio() -> List[str]:
        return []

    @staticmethod
    def test_prod_portfolio() -> List[str]:
        return Portfolio.test_portfolio() + Portfolio.prod_portfolio()

    @staticmethod
    def berkshire_hathaway_cnbc() -> Tuple[Any, ...]:
        url: str = 'https://docs.google.com/spreadsheet/tq?key=0AvnqqjtntdHRdENTQ283OGZTUWVMejRGTUVjZXphWlE'
        headers: Dict[str, str] = {'User-Agent': UserAgent().chrome}
        page: Response = requests.get(url, headers=headers)
        content: str = re.search(r'\((.*?)\)', page.text).group(1)
        data: Dict[str, Dict[str, List[str]]] = json.loads(content)
        return tuple(
            map(lambda e: e['c'][1]['v'], list(filter(lambda x: x['c'][1] is not None, data['table']['rows']))))

    @staticmethod
    def berkshire_hathaway_yahoo() -> Tuple[Any, ...]:
        url: str = 'https://finance.yahoo.com/u/yahoo-finance/watchlists/the-berkshire-hathaway-portfolio'
        headers: Dict[str, str] = {'User-Agent': UserAgent().chrome}
        page: Response = requests.get(url, headers=headers)
        doc = lh.fromstring(page.content)
        elements: List[lh.HtmlElement] = doc.xpath(
            '//*[@id="Col1-0-WatchlistDetail-Proxy"]/div/section[3]/div/div/table/tbody/tr/td[1]')
        return tuple(map(lambda e: e.text_content(), elements))

    @staticmethod
    def berkshire_hathaway_wikipedia() -> Tuple[str]:
        url: str = 'https://en.wikipedia.org/wiki/List_of_assets_owned_by_Berkshire_Hathaway'
        headers: Dict[str, str] = {'User-Agent': UserAgent().chrome}
        page: Response = requests.get(url, headers=headers)
        doc = lh.fromstring(page.content)
        elements = doc.xpath('//*[@id="mw-content-text"]/div/table[3]/tbody/tr/td[2]')
        return tuple(map(lambda e: re.sub(r'^.*?:', '', e.text_content()).strip(), elements))


if __name__ == '__main__':
    tickers: Tuple[str] = Portfolio.berkshire_hathaway_wikipedia()
    print(len(tickers))
    for ticker in tickers:
        print(ticker)
