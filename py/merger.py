import requests
import pandas as pd
def get_futures_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    data = requests.get(url).json()
    symbols = []
    for symbol in data['symbols']:
        symbols.append(symbol['symbol'])
    return symbols

futures_symbols = get_futures_symbols()

for symbol in futures_symbols:
    df = pd.read_csv('data/long_short_ratio/5m/' + symbol + '.csv')
    try:
        df1 = pd.read_csv('Trivix/data/long_short_ratio/5m/' + symbol + '.csv')
    except:
        df1 = df
    # Merge 2 file together
    # If there are rows from 2 files that have the same timestamp, keep the row from the first file
    # Otherwise add both data
    df = pd.concat([df, df1], ignore_index=True)
    # Sort by timestamp
    df = df.sort_values(by=['Timestamp'])
    if (symbol == "1000LUNCUSDT"):
        print(df)
    df = df.drop_duplicates(subset=['Timestamp'], keep='first')
    df.to_csv('data/long_short_ratio/5m/' + symbol + '.csv', index=False)