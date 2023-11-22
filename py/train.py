#%%
import pandas as pd
import numpy as np
import keras.metrics
import keras.losses
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import SGD
import joblib
from sklearn.model_selection import train_test_split
from py.market import *
pd.set_option('display.max_rows', None)
import time

# %%
def extract_data(arr):
    arr = arr * 1e7
    min_val = np.min(arr, axis=0)
    max_val = np.max(arr, axis=0)
    arr = (arr - min_val) / (max_val - min_val)
    return arr

# %%
def train_model(Xtrain, Xtest, ytrain, ytest, symbol, tp):
    CLS = 3 # Up, Sideway, down
    ytrain = np.eye(CLS)[ytrain.astype(int)]
    ytest = np.eye(CLS)[ytest.astype(int)]
    model = Sequential()
    model.add(LSTM(128, input_shape=(60, 6,), activation='tanh'))
    model.add(Dense(CLS, activation='softmax'))
    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(
        optimizer="rmsprop",
        loss="categorical_crossentropy",
        metrics=["categorical_accuracy"],
    )
    model.fit(Xtrain, ytrain, epochs=10, batch_size=32)
    y_pred = model.predict(Xtest)
    predict_labels = np.argmax(y_pred, axis=1)
    joblib.dump(model, 'model/short/5m/' + symbol)

# %%
def analyze_data(symbol):
    df = pd.read_csv(DIR + symbol + '.csv')
    tp = df['timestamp'].to_numpy()
    df = df[['open', 'high', 'low', 'close', 'volume', 'ratio']]
    arr = df.to_numpy()
    arr1 = extract_data(arr)
    input = []
    output = []
    TP = []
    cnt = [0, 0, 0]
    for i in range(0, len(arr) - 80):
        input.append(arr1[i : i + 60])
        TP.append(tp[i])
        maxx = 0
        minn = 1e9
        current = arr[i + 59][3]
        if (current == 0): exit()
        trend = 0
        for j in range(i + 60, i + 80):
            minn = min(minn, arr[j][2])
            maxx = max(maxx, arr[j][1])
            if (1.0 - minn / current > 0.01):
                trend = -1
                break
            if (maxx / current - 1 > 0.01):
                trend = 1
                break
        cnt[trend + 1] += 1
        output.append(trend + 1)
    input = np.array(input) 
    print(cnt)
    output = np.array(output)
    Xtrain, Xtest, ytrain, ytest = train_test_split(input, output, test_size=0.2, random_state=0)
    train_model(Xtrain, Xtest, ytrain, ytest, symbol, TP[len(ytrain) : ])
# %%
DIR = 'data/candles/5m/'
symbols = futures_exchange_information("SYMBOL")
print(symbols)
if __name__ == '__main__':
    import multiprocessing
    with multiprocessing.Pool() as pool:
        pool.starmap(analyze_data,  [(symbol,) for symbol in symbols])