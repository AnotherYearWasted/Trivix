#%%
import pandas as pd
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import SGD
import joblib
from py.market import *
# Load data
print(futures_open_interest_statistics('BTCUSDT', '5m', limit=500))
#%%
exit()
data = pd.read_csv('data/candles/1m/BTCUSDT.csv')
data = data[['close']]
# Preprocess data
# ...

# Split data into train and test sets
train_size = int(len(data) * 0.8)
train_data = data[:train_size]
test_data = data[train_size:].reset_index(drop=True)

# Define input and output variables
X_train, y_train = [], []
for i in range(20, len(train_data)):
    X_train.append(train_data.iloc[i-20:i, :].values)
    direction = 0 if train_data['close'][i] > train_data['close'][i-1] else 1
    strength = (train_data['close'][i] - train_data['close'][i-1]) / train_data['close'][i-1] * 100
    y_train.append([direction, strength])

X_train, y_train = np.array(X_train), np.array(y_train)

X_test, y_test = [], []
for i in range(20, len(test_data)):
    X_test.append(test_data.iloc[i-20:i, :].values)
    direction = 0 if test_data['close'][i] > test_data['close'][i-1] else 1
    strength = (test_data['close'][i] - test_data['close'][i-1]) / test_data['close'][i-1] * 100
    y_test.append([direction, strength])

X_test, y_test = np.array(X_test), np.array(y_test)

# Define the model architecture
model = Sequential()
model.add(LSTM(64, input_shape=(20, 1), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.add(Dense(1, activation='linear'))
# Compile the model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print(np.isnan(X_train).sum())
print(np.isnan(y_train).sum())
print(np.isnan(X_test).sum())
print(np.isnan(y_test).sum())
joblib.dump(model, 'model/short/model')