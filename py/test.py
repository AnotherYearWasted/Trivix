import websocket
import pandas as pd
ws = websocket.WebSocket()
ws.connect('wss://fstream.binance.com/ws')
import json

symbols = ['BTCUSDT']


for symbol in symbols:
    request = {
        "method": "SUBSCRIBE",
        "params": [
            str(symbol).lower() + "@kline_1m"
        ],
        "id": 1
    }

    ws.send(json.dumps(request))

while True:
        message = ws.recv()
        try:
            data = json.loads(message)
        except:
            continue
        
        if 'stream' in data:
            # This is a data message
            symbol = data['stream'].split('@')[0]
            kline = data['data']['k']
            print(f"{symbol}: Open={kline['o']}, High={kline['h']}, Low={kline['l']}, Close={kline['c']}")
        else:
            # This is a response message (not relevant for kline data)
            print(f"Received response: {data}")