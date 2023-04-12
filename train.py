#%%
import pandas as pd
import numpy as np
import keras.losses
from keras.models import Sequential
from keras.layers import Dense, LSTM
import joblib
from api.market import *
pd.set_option('display.max_rows', None)
import time 
import tensorflow as tf

#%%

def percent_loss(y_true, y_pred):
    diff = tf.abs(y_true - y_pred) / tf.abs(y_true)
    return 100.0 * tf.reduce_mean(diff)

intervals = [
    # (60, '1m', 1500),
    (300, '5m', 500),
    # (900, '15m', 100),
    # (86400, '1d', 10),
]
try:
    symbols = pd.read_csv('data/symbols.csv')
except:
    symbols = futures_exchange_information('SYMBOL')
    symbols = pd.DataFrame(symbols, columns='symbol')
    symbols.to_csv('data/symbols.csv')
symbols = symbols['symbol'].to_list()
symbols = ['FOOTBALLUSDT', 'BTCUSDT', 'DARUSDT']
try:
    general_model = joblib.load('model/short/5m/model')
    print('loaded general_model successfully')
except:
    general_model = Sequential()
    general_model.add(LSTM(64, input_shape=(20, 6), activation='relu'))
    general_model.add(Dense(32, activation='relu'))
    general_model.add(Dense(1, activation='linear'))
    general_model.compile(loss=percent_loss, optimizer='adam')

x_train = np.zeros((0, 20, 6))
y_train = np.zeros((0))

for symbol in symbols:
    for interval in intervals:
        print('Processing for', symbol, 'with interval', interval)
        data = pd.read_csv('data/candles/' + interval[1] + '/' + symbol + '.csv')
        df = data[['open', 'high', 'low', 'close', 'volume']]
        try:
            model = joblib.load('model/short/5m/' + symbol)
            print('loaded model successfully for', symbol)
        except:
            model = Sequential()
            model.add(LSTM(64, input_shape=(20, 6), activation='relu'))
            model.add(Dense(32, activation='relu'))
            model.add(Dense(1, activation='linear'))
            model.compile(loss=percent_loss, optimizer='adam')
        matrices = []
        labels = []
        for i in range(len(df) - 39):
            slice_df = df.iloc[i : i + 20].copy()
            close = float(df.iloc[i + 19]['close'])
            maxx = 0
            for j in range(0, 20):
                slice_df['bars'] = j + 1
                maxx = max(maxx, float(df.iloc[i + 20 + j]['high']))
                low = df.iloc[i + 20 + j]['low']
                risk = maxx / close * 100 - 100
                labels.append(low)
                matrices.append(slice_df.to_numpy())
        X = np.array(matrices)
        labels = np.array(labels)
        print('data sucessfully processed')
        starttime = time.time()
        model.fit(X, labels, epochs=30, batch_size=20)
        joblib.dump(model, 'model/short/5m/' + symbol)
        x_train = np.concatenate((x_train, X))
        y_train = np.concatenate((y_train, labels))
        endtime = time.time()
        print('Time elapsed:', endtime - starttime)

print(x_train.shape, y_train.shape)
starttime = time.time()
general_model.fit(x_train, y_train, epochs=30, batch_size=32)
endtime = time.time()
print('Time elapsed:', endtime - starttime)
joblib.dump(general_model, 'model/short/5m/model')