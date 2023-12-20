import httpx
import json
import pandas as pd
import zipfile
import datetime, io, os
from typing import Literal
import asyncio
from market import futures_exchange_information

client = httpx.AsyncClient(timeout=None)

# url may look like this
# https://data.binance.vision/data/futures/um/daily/markPriceKlines/BTCUSDT/1m/BTCUSDT-1m-2023-12-12.zip
# Get data daily from the last 30 days
async def get_klines(symbol: str, 
             date: str, 
             func: Literal["klines", "markPriceKlines", "premiumIndexKlines", "indexPriceKlines"]
             ) -> pd.DataFrame:
    url = f'https://data.binance.vision/data/futures/um/daily/{func}/{symbol}/1m/' + symbol + '-1m-' + date + '.zip'
    """download content from a url, unzip, and save to a csv file"""
    r = await client.get(url)
    print(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f'data/{func}/')
    df = pd.read_csv(f'data/{func}/' + symbol + '-1m-' + date + '.csv')
    df.to_csv(f'data/{func}/' + symbol + '-1m-' + date + '.csv')
    # Delete the csv file
    os.remove(f'data/{func}/' + symbol + '-1m-' + date + '.csv')
    return df

# https://data.binance.vision/data/futures/um/daily/metrics/1000BONKUSDT/1000BONKUSDT-metrics-2023-12-12.zip
async def get_metrics(symbol: str,
                date: str,
                func: Literal["metrics", "liquidationSnapshot", "trades", "aggTrades","bookDepth", "bookTicker"]
                ) -> pd.DataFrame:
    try:
        url = f'https://data.binance.vision/data/futures/um/daily/{func}/{symbol}/' + symbol + '-' + func + '-' + date + '.zip'
        """download content from a url, unzip, and save to a csv file"""
        r = await client.get(url)
        print(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(f'data/{func}/')
        df = pd.read_csv(f'data/{func}/' + symbol + '-' + func + '-' + date + '.csv')
        df.to_csv(f'data/{func}/' + symbol + '-' + func + '-' + date + '.csv')
        # Delete the csv file
        os.remove(f'data/{func}/' + symbol + '-' + func + '-' + date + '.csv')
    except:
        df = pd.DataFrame()
    return df



async def get_daily_data_single(symbol: str, func: str, days: int):
    """get daily data from the last 30 days"""
    today = datetime.datetime.today()
    symbol = symbol
    func = func
    df = pd.DataFrame()
    tasks = []
    for i in range(2, 2 + days):
        date = today - datetime.timedelta(days=i)
        date = date.strftime('%Y-%m-%d')
        tasks.append(asyncio.create_task(get_klines(symbol, date, func)))
    
    # Wait for all tasks to complete
    responses = await asyncio.gather(*tasks)
    # Sort the data by the first column
    for response in responses:
        df = pd.concat([df, response])
    df.sort_values(by=df.columns[0], inplace=True)
    print(df)
    # Write data to csv file
    df.to_csv(f'data/{func}/' + symbol + '.csv', index=False)

async def get_daily_data(symbols):
    tasks = []
    for symbol in symbols:
        tasks.append(asyncio.create_task(get_daily_data_single(symbol, "klines", 30)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    symbols = futures_exchange_information("SYMBOL")
    asyncio.run(get_daily_data(symbols))