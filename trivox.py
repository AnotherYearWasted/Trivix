#%%
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from joblib import dump, load
import getdata
pd.set_option('display.max_rows', None)

#%%
# load the data
data = pd.read_csv('data/candles/1m.csv')
data['percentage'] = data['close'] / data['open'] - 1
data = data['percentage'] * 100
print(data)
data = data.values.reshape(-1, 1)
#%%
# perform clustering
kmeans = KMeans(n_clusters=30, random_state=0, n_init=10).fit(data)
labels = kmeans.labels_

# calculate frequency
hist, edges = np.histogram(data, bins=20)

# train linear regression model
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=0)
regressor = LinearRegression()
regressor.fit(X_train, y_train)


while True:
    y = float(input())
    # predict percentage and ideal time
    for i in range(1, 101):
        y.append(i / 100.0)
    y = np.array(y).reshape(-1,1)
    y_pred = regressor.predict(y)
    print(y_pred)
    print(kmeans.predict(y))
    x = float(input())
    # x is the input that I tell if the code run correctly to the data. If it's not, it should be train again. So write me a code below for that
