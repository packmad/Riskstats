from typing import Tuple, List, Dict

import yfinance as yf
import pandas as pd
from datetime import datetime
from os.path import join, isfile, isdir
from hurst import compute_Hc


DB_DIR = 'DBcsv'
assert isdir(DB_DIR)


class Asset:
    def __init__(self, ticker_symbol: str, name: str, start: int, end: int):
        self.ticker_symbol = ticker_symbol
        self.db_file = join(DB_DIR, f'{ticker_symbol}.csv')
        self.name = name
        self.start_date = datetime.fromtimestamp(start)
        self.end_date = datetime.fromtimestamp(end)
        self.history = None
        self.hurst_scale_factor = None
        self.hurst_exponent = None

    def get_history(self) -> pd.DataFrame:
        if self.history is not None:
            return self.history
        if isfile(self.db_file):
            self.history = pd.read_csv(self.db_file)
        else:
            ticker = yf.Ticker(self.ticker_symbol)
            self.history = ticker.history(start=self.start_date, end=self.end_date, interval="1d")
            self.history.to_csv(self.db_file)
        assert self.history is not None
        return self.history

    def get_closing_prices(self):
        return self.get_history()['Close']

    def get_hurst(self) -> Tuple[float, float, List]:
        h, c, d = compute_Hc(self.get_closing_prices(), kind='price', simplified=True)
        self.hurst_exponent = h
        self.hurst_scale_factor = c
        return h, c, d

    def toJSON(self) -> Dict:
        if self.hurst_exponent is None:
            _ = self.get_hurst()
        return {
            'ticker': self.ticker_symbol,
            'name': self.name,
            'hurst_scale_factor': self.hurst_scale_factor,
            'hurst_exponent': self.hurst_exponent,
        }


def main():
    assets = list()
    assets.append(
        Asset('BTC-USD', 'Bitcoin USD (BTC-USD)', 1410912000, 1730850352)
    )
    assets.append(
        Asset('VWCE.DE', 'Vanguard FTSE All-World UCITS ETF USD Acc', 1564383600, 1730850519)
    )
    assets.append(
        Asset('IVV', 'iShares Core S&P 500 ETF (IVV)', 958743000, 1730937600)
    )
    assets.append(
        Asset('NVDA', 'NVIDIA Corporation (NVDA)', 917015400, 1731085318)
    )
    assets.append(
        Asset('TSLA', 'Tesla, Inc. (TSLA)', 1277818200, 1731085300)
    )
    df = pd.DataFrame([j.toJSON() for j in assets])
    print(df.sort_values(by='hurst_exponent', ascending=False).to_markdown())


if __name__ == '__main__':
    main()
