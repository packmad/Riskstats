import yfinance as yf
import pandas as pd

from scipy.stats import pearsonr
from datetime import date
from assets import AssetsManager, Asset


AM = AssetsManager()


def hurst_rank():
    df = pd.DataFrame([j.toJSON() for j in AM.assets])
    print(df.sort_values(by='hurst_exponent', ascending=False).to_markdown())


def pearson_correlation(asset1: Asset, asset2: Asset):
    print(f'Pearson correlation: "{asset1.name}" vs. "{asset2.name}"')
    df1 = asset1.get_history()
    df2 = asset2.get_history()
    df1['Date'] = pd.to_datetime(df1['Date'], utc=True)
    df2['Date'] = pd.to_datetime(df2['Date'], utc=True)
    df1['Date_Only'] = df1['Date'].dt.date
    df2['Date_Only'] = df2['Date'].dt.date
    common_dates = set(df1['Date_Only']).intersection(set(df2['Date_Only']))
    for i in range(2015, 2025):
        common_dates_range = {d for d in common_dates if date(i, 1, 1) <= d <= date(i, 12, 31)}
        filtered_df1 = df1[df1['Date_Only'].isin(common_dates_range)]
        filtered_df2 = df2[df2['Date_Only'].isin(common_dates_range)]
        merged_df = pd.merge(filtered_df1, filtered_df2, on='Date_Only', suffixes=('_df1', '_df2'))
        filtered_df1_close = merged_df['Close_df1'].to_numpy()
        filtered_df2_close = merged_df['Close_df2'].to_numpy()
        stat, pvalue = pearsonr(filtered_df1_close, filtered_df2_close)
        if pvalue < 0.01:
            print(f'{i}', round(stat, 2))
        else:
            print(f'{i}', '!pvalue!')
    print()


if __name__ == '__main__':
    print(f"yfinance version='{yf.__version__}'")

    pearson_correlation(AM.get_asset('BTC-USD'), AM.get_asset('IVV'))
    pearson_correlation(AM.get_asset('BTC-USD'), AM.get_asset('GC%3DF'))

    hurst_rank()
