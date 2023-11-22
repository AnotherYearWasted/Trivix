import json
import csv
import asyncio
import websockets
import traceback
from market import futures_exchange_information, futures_klines, futures_long_short_ratio
stack = {}

def reset_data(symbol):
    global stack
    stack.update(
        {
            symbol : {
                "time" : 0,
                "buy_liq_count" : 0,
                "sell_liq_count" : 0,
                "buy_liq_quantity" : 0,
                "sell_liq_quantity" : 0,
                "total_liq_quantity" : 0,
                "total_liq_count": 0,
                "avg_buy_price": 0,
                "avg_sell_price": 0,
                "total_order_count": 0,
            }
        }
    )


def on_message(data):
    global stack
    data = data['data']
    EventType = data['e']
    if EventType == "kline":
        symbol = data['s']
        # if str(symbol) != coins[cnt]:
        #     print(symbol,coins[cnt],cnt)
        #     exit()
        interval = data['k']['i']
        open_price = data['k']['o']
        close_price = float(data['k']['c'])
        high_price = data['k']['h']
        low_price = data['k']['l']
        volume = data['k']['v']
        close_price = float(close_price)
        open_price = float(open_price)
        percent_change_1m = (close_price / open_price - 1) * 100
        percent_change_5m = 0
        percent_change_15m = 0
        print(symbol, close_price, percent_change_1m, percent_change_5m, percent_change_15m)
        if symbol not in stack:
            stack.update({symbol : []})
            stack[symbol].append(close_price)      
        if len(stack[symbol]) > 5:      
            percent_change_5m = (close_price / stack[symbol][-5 * 60 * 4] - 1) * 100
        if len(stack[symbol]) > 15:
            percent_change_15m = (close_price / stack[symbol][-15 * 60 * 4] - 1) * 100

        if len(stack[symbol]) > 60 *15 * 4:
            stack[symbol].pop(0)
    elif EventType == 'forceOrder':
        symbol = data['o']['s']
        side = data['o']['S']
        original_quantity = data['o']['q']
        executed_quantity = data['o']['l']
        current_time = data['o']['T']
        current_minute = int(current_time / 60000)
        if symbol not in stack:
            reset_data(symbol)
        if side == 'BUY':
            stack[symbol]['buy_liq_count'] += 1
            stack[symbol]['buy_liq_quantity'] += float(original_quantity)
        else:
            stack[symbol]['sell_liq_count'] += 1
            stack[symbol]['sell_liq_quantity'] += float(original_quantity)
        stack[symbol]['total_liq_count'] += 1
        stack[symbol]['total_liq_quantity'] += float(original_quantity)
        if current_minute != stack[symbol]['time']:
            # Write data to csv file
            with open(f'data/candles/1m/{symbol}.csv', 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    current_minute * 60,
                    stack[symbol]['buy_liq_count'],
                    stack[symbol]['sell_liq_count'],
                    stack[symbol]['buy_liq_quantity'],
                    stack[symbol]['sell_liq_quantity'],
                    stack[symbol]['total_liq_quantity'],
                    stack[symbol]['total_liq_count'],
                    stack[symbol]['avg_buy_price'],
                    stack[symbol]['avg_sell_price'],
                    stack[symbol]['total_order_count']
                ])
            reset_data(symbol)
        stack[symbol]['time'] = current_minute

    elif EventType == 'bookTicker':
        symbol = data['s']
        bid_price = data['b']
        ask_price = data['a']
        current_time = data['T']
        current_minute = int(current_time / 60000)
        if symbol not in stack:
            reset_data(symbol)
        stack[symbol]['avg_buy_price'] = (stack[symbol]['avg_buy_price'] * stack[symbol]['total_order_count'] + float(bid_price)) / (stack[symbol]['total_order_count'] + 1)
        stack[symbol]['avg_sell_price'] = (stack[symbol]['avg_sell_price'] * stack[symbol]['total_order_count'] + float(ask_price)) / (stack[symbol]['total_order_count'] + 1)
        stack[symbol]['total_order_count'] += 1
        if current_minute != stack[symbol]['time']:
            # Write data to csv file
            with open(f'data/candles/1m/{symbol}.csv', 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    current_minute * 60, 
                    stack[symbol]['buy_liq_count'], 
                    stack[symbol]['sell_liq_count'], 
                    stack[symbol]['buy_liq_quantity'], 
                    stack[symbol]['sell_liq_quantity'], 
                    stack[symbol]['total_liq_quantity'], 
                    stack[symbol]['total_liq_count'], 
                    stack[symbol]['avg_buy_price'], 
                    stack[symbol]['avg_sell_price'], 
                    stack[symbol]['total_order_count']
                ])
            reset_data(symbol)
        stack[symbol]['time'] = current_minute
        
async def connect_to_websocket(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            on_message(data)
            #print(data)

async def main():
    try:
        symbols = futures_exchange_information('SYMBOL')
        streams = ""
        for symbol in symbols:
            streams +=  symbol.lower() + '@forceOrder' + '/'
        streams += '!bookTicker'
        uris = [f"wss://fstream.binance.com/stream?streams={streams[1:]}"]
        print(uris)
        tasks = [connect_to_websocket(uri) for uri in uris]
        await asyncio.gather(*tasks)
    except Exception as e:
        print(str(e) + '\n')
        print(str(traceback.format_exc()) + '\n\n\n')
        await main()
asyncio.run(main())

