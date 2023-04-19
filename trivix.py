#%%
import pandas as pd
import numpy as np
import joblib
from keras.models import Sequential
from keras.layers import Dense
from api.market import *
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

symbol = 'DOGEUSDT'
model = joblib.load('model/short/5m/' + symbol)
df = pd.DataFrame(futures_klines(symbol, '5m', limit=500))
df1 = pd.DataFrame(futures_long_short_ratio(symbol, '5m', limit=500))
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
arr = df[['open', 'high', 'low', 'close', 'volume', 'ratio']].to_numpy()

Xtest = []
for i in range(0, 481):
    Xtest.append(arr[i : i + 20])
Xtest = np.array(Xtest)
y_pred = model.predict(extract_data(Xtest.astype(float)))

df1['timestamp'] = pd.to_datetime(df1['timestamp'] + 1000 * 7 * 60 * 60 + 300, unit='ms')
df1['timestamp'] = df1['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
for i in range(0, len(y_pred)):
    print(y_pred[i], df1.iloc[i + 19]['timestamp'])
print(len(y_pred))