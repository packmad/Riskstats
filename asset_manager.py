from typing import List, Optional

from asset import Asset


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
            Asset('0P0001AKPA.F', 'CM-AM Avenir Monétaire')  # r1
        )
        self.assets.append(
            Asset('0P0001AKP8.F', 'CM-AM Avenir Tempéré')  # r2
        )
        self.assets.append(
            Asset('F00000WACN.PA', 'Social Active Tempéré Solidaire')  # r2
        )
        self.assets.append(
            Asset('0P00016NIO.F', 'Social Active Tempéré Solidaire C')  # r2
        )
        self.assets.append(
            Asset('0P00016NKU.F', 'CM-AM Perspective Certitude')  # r2
        )
        self.assets.append(
            Asset('0P0001AKP7.F', 'CM-AM Avenir Oblig')  # r2
        )
        self.assets.append(
            Asset('0P0001AKP6.F', 'CM-AM Avenir Equilibre')  # r3
        )
        self.assets.append(
            Asset('0P0001AKP5.F', 'CM-AM Avenir Actions International')  # r4
        )
        self.assets.append(
            Asset('0P0001AKOX.F', 'CM-AM Avenir Actions Europe')  # r4
        )
        self.assets.append(
            Asset('0P0001AKP9.F', 'CM-AM Avenir Dynamique')  # r4
        )
        self.assets.append(
            Asset('0P0001AKP2.F', 'CM-AM Avenir Actions France')  # r5
        )


    def get_asset(self, ticker: str) -> Optional[Asset]:
        for asset in self.assets:
            if asset.ticker_symbol == ticker:
                return asset
        assert False, 'Asset not found'
