import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import sys
import os.path

if len(sys.argv) < 2:
    print("Usage: python py/plot.py <symbol>")
    exit()

symbol = sys.argv[1]
symbol = symbol.upper()
csv_file_path = 'data/long_short_ratio/5m/'
csv_file_name = symbol + ".csv"

# Check if file or directory exists
if not os.path.isfile(csv_file_path + csv_file_name):
    print("No such file or directory: " + csv_file_path + csv_file_name)
    exit()

df = pd.read_csv(csv_file_path + csv_file_name)

# Convert timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
# Intervel is 5 minute, we need to change to 1 minute interval by adding 4 rows between each row
df = df.reindex(index=df.index.repeat(5)).reset_index(drop=True)
df['Timestamp'] = df['Timestamp'] + pd.to_timedelta(df.groupby(level=0).cumcount(), unit='m')

# Import candlestick data
df_candlestick = pd.read_csv('data/candles/1m/' + csv_file_name)

# Convert timestamp to datetime
df_candlestick['Timestamp'] = pd.to_datetime(df_candlestick['Open Time'], unit='ms')


merged_df = pd.merge(df, df_candlestick, on='Timestamp', how='inner')
df = merged_df
df_kill = pd.read_csv('data/liquidations/' + csv_file_name)
# Liquidation timestamp is random, so we will count the number of liquidation in each 1 minute interval
df_kill['Timestamp'] = pd.to_datetime(df_kill['Time'], unit='ms')
df_kill['Timestamp'] = df_kill['Timestamp'].dt.floor('min')
df_kill = df_kill.groupby('Timestamp').size().reset_index(name='Liquidation')
df = pd.merge(df, df_kill, on='Timestamp', how='left')
df['Liquidation'] = df['Liquidation'].fillna(0)
# Get max value of liquidation
max_liquidation = df['Liquidation'].max()
# Divide liquidation by max liquidation to get a ratio
df['Liquidation'] = df['Liquidation'] / max_liquidation
# Multiply by max value of volume to get a value that is comparable to volume
df['Liquidation'] = df['Liquidation'] * df['Volume'].max()
x_values = df['Timestamp']
y_values1 = df[' GlobalLongAcc']
y_values2 = df[' GlobalShortAcc']

fig, (ax1, ax3) = plt.subplots(2, 1, sharex=True, figsize=(24, 12), gridspec_kw={'hspace': 0})

color = 'tab:blue'
ax1.set_xlabel('Datetime')
ax1.set_ylabel('Long - Short', color=color)
ax1.plot(x_values, y_values1 - y_values2, color=color, linestyle='-', marker='o', markersize=3, markerfacecolor='yellow')
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('MainPrice', color=color)  # we already handled the x-label with ax1
ax2.plot(x_values, df['Close'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# New subplot for volume and open interest
color = 'tab:blue'
ax3.set_xlabel('Datetime')
ax3.set_ylabel('Volume', color=color)
ax3.plot(x_values, df['Volume'], color=color, linestyle='-', marker='o', markersize=3, markerfacecolor='yellow')
ax3.tick_params(axis='y', labelcolor=color)
ax3.plot(x_values, df['Liquidation'], color='tab:orange', linestyle='-', marker='o', markersize=3, markerfacecolor='yellow')
ax3.tick_params(axis='y', labelcolor=color)


ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax4.set_ylabel('Open Interest', color=color)  # we already handled the x-label with ax3
ax4.plot(x_values, df['Open Interest'], color=color)
ax4.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title(symbol)
plt.grid(True)
plt.legend()
plt.savefig('data/plots/' + symbol + '.png')
print('Plot saved to data/plots/' + symbol + '.png')