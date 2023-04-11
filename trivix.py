#%%
import pandas as pd
import numpy as np
import joblib
from keras.models import Sequential
from keras.layers import Dense
from api.market import *
pd.set_option('display.max_rows', None)
import time

# %%
model = joblib.load('model/short/1m/BTCUSDT')
df = pd.DataFrame(futures_klines('BTCUSDT', '1m', limit=20))
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
df = df[['open', 'high', 'low', 'close', 'volume']]
arr = []
for i in range(1, 2):
    df['bars'] = i
    arr.append(df.astype(np.float32).to_numpy())

print(df)

print(model.predict(np.array(arr)))