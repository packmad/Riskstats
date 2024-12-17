from typing import Tuple, List, Dict, Optional

import yfinance as yf
import pandas as pd
from datetime import datetime
from os.path import join, isfile, isdir

from pandas import Series
from hurst import compute_Hc


DB_DIR = 'DBcsv'
assert isdir(DB_DIR)


class Asset:
    def __init__(self, ticker_symbol: str, name: str):
        self.ticker_symbol = ticker_symbol
        self.db_file = join(DB_DIR, f'{ticker_symbol}.csv')
        self.name = name
        self.history = None
        self.hurst_scale_factor = None
        self.hurst_exponent = None

    def get_history(self) -> pd.DataFrame:
        if self.history is not None:
            return self.history
        if not isfile(self.db_file):
            yf_history = yf.Ticker(self.ticker_symbol).history(period="max", interval="1d", raise_errors=True)
            yf_history.to_csv(self.db_file)
        self.history = pd.read_csv(self.db_file)
        assert self.history is not None
        return self.history

    def get_closing_prices(self) -> Series:
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


class AssetsManager:
    assets: List[Asset]

    def __init__(self):
        self.assets = list()
        self.assets.append(
            Asset('GC%3DF', 'Gold USD')
        )
        self.assets.append(
            Asset('BTC-USD', 'Bitcoin USD')
        )
        self.assets.append(
            Asset('VWCE.DE', 'Vanguard FTSE All-World UCITS ETF USD Acc')
        )
        self.assets.append(
            Asset('IVV', 'iShares Core S&P 500 ETF (IVV)')
        )
        self.assets.append(
            Asset('NVDA', 'NVIDIA Corporation (NVDA)')
        )
        self.assets.append(
            Asset('TSLA', 'Tesla, Inc. (TSLA)')
        )
        self.assets.append(
            Asset('EXW1.DE', 'iShares Core EURO STOXX 50 UCITS ETF')
        )
        self.assets.append(
            Asset('URTH', 'iShares MSCI World ETF (URTH)')
        )
        self.assets.append(
            Asset('0P0001AKP8.F', 'CM-AM Avenir Tempéré')  # r2
        )
        self.assets.append(
            Asset('0P0001AKP6.F', 'CM-AM Avenir Equilibre')  # r3
        )
        self.assets.append(
            Asset('F00000WACN.PA', 'Social Active Tempéré Solidaire')  # r2
        )
        self.assets.append(
            Asset('0P0001AKPA.F', 'CM-AM Avenir Monétaire')  # r1
        )
        self.assets.append(
            Asset('0P00016NKU.F', 'CM-AM Perspective Certitude')  # r2
        )
        self.assets.append(
            Asset('0P0001AKP7.F', 'CM-AM Avenir Oblig')  # r2
        )
        self.assets.append(
            Asset('0P0001AKP5.F', 'CM-AM Avenir Actions International')  # r4
        )
        self.assets.append(
            Asset('0P0001AKOX.F', 'CM-AM Avenir Actions Europe')  # r4
        )
        self.assets.append(
            Asset('0P0001AKP2.F', 'CM-AM Avenir Actions France')  # r5
        )
        self.assets.append(
            Asset('0P0001AKP9.F', 'CM-AM Avenir Dynamique')  # r4
        )

    def get_asset(self, ticker: str) -> Optional[Asset]:
        for asset in self.assets:
            if asset.ticker_symbol == ticker:
                return asset
        assert False, 'Asset not found'
