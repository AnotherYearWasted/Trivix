# %%
from api.market import *
import pandas as pd

# %%
df = pd.DataFrame(futures_klines('DOGEUSDT', '1m', limit=1000))

df.columns = [
    'open time', 
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

df.to_csv(r'data/candles/1m.csv', index=False)

# %%
dataset = pd.read_csv('data/candles/1m.csv')
