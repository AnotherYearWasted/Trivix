import websocket
import json
import time
import alert

alert.telegram_bot_sendtext("...safd.")
cnt = -1
coinmx = ""
valmx = -1 
def on_open(ws):
    streams = [f"{coin.lower()}@kline_5m" for coin in coins]
    #streams = [f"{coin}@kline_5m" for coin in coins]
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": streams,
        "id": 1
    }))
exit()
def on_message(ws, message):
    #print(cnt)
    data = json.loads(message)    
    symbol = data['s']
    #print(str(symbol))
    '''if str(symbol) != coins[cnt]:
        print(symbol,coins[cnt],cnt)
        exit()'''
    print(data)
    interval = data['k']['i']
    open_price = data['k']['o']
    close_price = data['k']['c']
    high_price = data['k']['h']
    low_price = data['k']['l']
    low_price = float(low_price)
    volume = data['k']['v']
    print(inform65, low_price, 1.65)
    if low_price <= 1.65 and not inform65:
        telegram_bot_sendtext('COCOSUSDT Reached 1\.75')
        inform65 = True
    if low_price <= 1.60 and not inform60:
        telegram_bot_sendtext('COCOSSDT reached 1\.60')
        inform60 = True
        
    
def on_close(ws):
    print("WebSocket connection is closed.")

socket = "wss://fstream.binance.com/ws/"
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)

ws.run_forever()