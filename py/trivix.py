#%%
import pandas as pd
import numpy as np
import joblib
from keras.models import Sequential
from keras.layers import Dense
from py.market import *
import tensorflow as tf
pd.set_option('display.max_rows', None)
np.set_printoptions(threshold=np.inf)
import time
# %%

def extract_data(arr):
    min_val = np.min(arr, axis=0)
    max_val = np.max(arr, axis=0)
    arr = (arr - min_val) / (max_val - min_val)
    return arr

symbol = 'TOMOUSDT'
model = joblib.load('model/short/5m/' + symbol)
df = pd.DataFrame(futures_klines(symbol, '5m', limit=499))
df1 = pd.DataFrame(futures_long_short_ratio(symbol, '5m', limit=499))
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
df1.columns = [
    'timestamp',
    'ratio'
]
df['ratio'] = df1['ratio']
lastdf = pd.read_csv('data/candles/5m/' + symbol + '.csv')
lastdf = lastdf[lastdf['timestamp'] < df.iloc[0]['timestamp']]
df = pd.concat([lastdf, df], ignore_index=True)
arr = df[['open', 'high', 'low', 'close', 'volume', 'ratio']].to_numpy().astype(float)
arr1 = extract_data(arr)
Xtest = []

for i in range(0, len(arr1) - 59):
    Xtest.append(arr1[i : i + 60])
Xtest = np.array(Xtest)
y_pred = model.predict(Xtest)
df['timestamp'] = pd.to_datetime(df['timestamp'] + 1000 * 7 * 60 * 60 + 300, unit='ms')
df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
for i in range(0, len(y_pred)):
    trend = 0
    maxx = 0
    minn = 1e9
    current = arr[i + 59][3]
    for j in range(i + 60, i + 80):
        if (current == 0): exit()
        if (j < len(arr)):
            minn = min(minn, arr[j][2])
            maxx = max(maxx, arr[j][1])
            if (1.0 - minn / current > 0.01):
                trend = -1
                break
            if (maxx / current - 1 > 0.01):
                trend = 1
                break
        else:
            trend = 'unknown'
    print(y_pred[i], df.iloc[i + 19]['timestamp'], trend)
