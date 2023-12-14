import requests
import json
import pandas as pd
import zipfile
import datetime, io, os
from typing import Literal

# url may look like this
# https://data.binance.vision/data/futures/um/daily/markPriceKlines/BTCUSDT/1m/BTCUSDT-1m-2023-12-12.zip
# Get data daily from the last 30 days
def get_klines(symbol: str, 
             date: str, 
             func: Literal["klines", "markPriceKlines", "premiumIndexKlines", "indexPriceKlines"]
             ) -> pd.DataFrame:
    url = f'https://data.binance.vision/data/futures/um/daily/{func}/{symbol}/1m/' + symbol + '-1m-' + date + '.zip'
    """download content from a url, unzip, and save to a csv file"""
    r = requests.get(url)
    print(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f'data/{func}/')
    df = pd.read_csv(f'data/{func}/' + symbol + '-1m-' + date + '.csv')
    df.to_csv(f'data/{func}/' + symbol + '-1m-' + date + '.csv')
    # Delete the csv file
    os.remove(f'data/{func}/' + symbol + '-1m-' + date + '.csv')
    return df

# https://data.binance.vision/data/futures/um/daily/metrics/1000BONKUSDT/1000BONKUSDT-metrics-2023-12-12.zip
def get_metrics(symbol: str,
                date: str,
                func: Literal["metrics", "liquidationSnapshot", "trades", "aggTrades","bookDepth", "bookTicker"]
                ) -> pd.DataFrame:
    url = f'https://data.binance.vision/data/futures/um/daily/{func}/{symbol}/' + symbol + '-' + func + '-' + date + '.zip'
    """download content from a url, unzip, and save to a csv file"""
    r = requests.get(url)
    print(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f'data/{func}/')
    df = pd.read_csv(f'data/{func}/' + symbol + '-' + func + '-' + date + '.csv')
    df.to_csv(f'data/{func}/' + symbol + '-' + func + '-' + date + '.csv')
    # Delete the csv file
    os.remove(f'data/{func}/' + symbol + '-' + func + '-' + date + '.csv')
    return df

def get_daily_data():
    """get daily data from the last 30 days"""
    today = datetime.datetime.today()
    symbol = 'BTCUSDT'
    func = 'klines'
    df = pd.DataFrame()
    for i in range(2, 366):
        date = today - datetime.timedelta(days=i)
        date = date.strftime('%Y-%m-%d')
        df1 = get_klines(symbol, date, func)
        # Concatenate dataframes
        df = pd.concat([df, df1])
    # Sort the data by the first column
    print(df)
    df.sort_values(by=df.columns[0], inplace=True)
    # Write data to csv file
    df.to_csv(f'data/{func}/' + symbol + '.csv', index=False)

get_daily_data()