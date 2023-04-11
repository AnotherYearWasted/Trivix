# %%
from api.market import *
import pandas as pd
import time

#%%
intervals = [
    (60, '1m', 1500),
    (300, '5m', 500),
    (900, '15m', 100),
    (86400, '1d', 10),
]
try:
    asymbols = pd.read_csv('data/symbols.csv')
except:
    asymbols = futures_exchange_information('SYMBOL')
    asymbols = pd.DataFrame(asymbols, columns='symbol')
    asymbols.to_csv('data/symbols.csv')
asymbols = asymbols['symbol'].to_list()
#%%
def pre_processing():
    for i in range(0, len(asymbols), 100):
        symbols = asymbols[i:min(i + 100, len(asymbols))]
        periods = []
        data = []
        for interval in intervals:
            data.append(futures_klines(symbols, [interval[1]], limit=interval[2], asynchronous=1))
            periods.append(interval[1])
            #time.sleep(60)
        for j, dat1 in enumerate(data):
            for i, list in enumerate(dat1):
                df = pd.DataFrame(list)
                df.columns = [
                    'timestamp', 
                    'open', 
                    'high', 
                    'low', 
                    'close', 
                    'volume', 
                    'close time', 
                    'Quote assest volume', 
                    'Number of Trades', 
                    'Taker BAV', 
                    'Taker QAV', 
                    'Unused field'
                ]
                try:
                    lastdf = pd.read_csv('data/candles/' + periods[j] + '/' + symbols[i] + '.csv')
                except:
                    lastdf = df
                lastdf = lastdf[lastdf['timestamp'] < df.iloc[0]['timestamp']]
                df = pd.concat([lastdf, df], ignore_index=True)
                df.to_csv('data/candles/' + periods[j] + '/' + symbols[i] + '.csv', index=False)
        time.sleep(60)
pre_processing()
symbols = asymbols
while True:
    current = time.time()
    time.sleep(60 - current % 60)
    current = int(current / 60) * 60
    periods = []
    for interval in intervals:
        if current % interval[0] == 0:
            periods.append(interval[1])
    data = futures_klines(symbols, periods, limit=100, asynchronous=1)
    for i, list in enumerate(data):
        j = i % len(periods)
        i = int(i / len(periods))
        df = pd.DataFrame(list)
        df.columns = [
            'timestamp', 
            'open', 
            'high', 
            'low', 
            'close', 
            'volume', 
            'close time', 
            'Quote assest volume', 
            'Number of Trades', 
            'Taker BAV', 
            'Taker QAV', 
            'Unused field'
        ]
        try:
            lastdf = pd.read_csv('data/candles/' + periods[j] + '/' + symbols[i] + '.csv')
        except:
            lastdf = df
        lastdf = lastdf[lastdf['timestamp'] < df.iloc[0]['timestamp']]
        df = pd.concat([lastdf, df], ignore_index=True)
        df.to_csv('data/candles/' + periods[j] + '/' + symbols[i] + '.csv', index=False)