#%%
import pandas as pd
import numpy as np
import joblib
from keras.models import Sequential
from keras.layers import Dense
from api.market import *
import tensorflow as tf
pd.set_option('display.max_rows', None)
import time
# %%


def percent_loss(y_true, y_pred):
    diff = tf.abs(y_true - y_pred) / tf.abs(y_true)
    return 100.0 * tf.reduce_mean(diff)

model = joblib.load('model/short/5m/FOOTBALLUSDT')
general_model = joblib.load('model/short/5m/model')
df = pd.DataFrame(futures_klines('FOOTBALLUSDT', '5m', limit=30))
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
df = df.iloc[:20]
arr = []
for i in range(1, 2):
    df['bars'] = i
    arr.append(df.astype(np.float32).to_numpy())

print(df)

x = model.predict(np.array(arr))
y = general_model.predict(np.array(arr))

print(x, y, (x + y) / 2)