# %%
import requests
import asyncio
import aiohttp
from urllib.parse import urlencode
from typing import Literal, Union

# %%
SPOT_API_URL = 'https://api.binance.com/api/v3'
FUTURES_API_URL = 'https://fapi.binance.com/fapi/v1'

# %%

def futures_klines(symbol: Union[str, list[str]], interval: Union[str, list[str]], startTime=None, endTime=None, limit=500, asynchronous=False):
    url = FUTURES_API_URL + '/klines'
    if not asynchronous:
        if (startTime): startTime = int(startTime * 1000)
        if (endTime) : endTime = int(endTime * 1000)
        params = {
            'symbol' : symbol,
            'interval' : interval,
            'startTime' : startTime,
            'endTime' : endTime,
            'limit' : limit
        }
        response = requests.get(url, params=params).json()
        return response
    else:
        ret = []
        # Asynchronous API call
        async def get_klines(symbols, intervals, startTime, endTime, limit):
            async with aiohttp.ClientSession(trust_env=True) as session:
                tasks = []
                for symbol in symbols:
                    for interval in intervals:
                        if (startTime): startTime = int(startTime * 1000)
                        if (endTime) : endTime = int(endTime * 1000)
                        params = {
                            'symbol' : symbol,
                            'interval' : interval,
                            'startTime' : startTime,
                            'endTime' : endTime,
                            'limit' : limit
                        }
                        URL = url + '?' + urlencode(params)
                        tasks.append(asyncio.create_task(session.get(URL, ssl=False)))
                responses = await asyncio.gather(*tasks)
                print('gathered')
                for response in responses:
                    ret.append(await response.json())
                print('done')
            return ret
        return asyncio.run(get_klines(symbol, interval, startTime, endTime, limit))
# %%
def futures_continuousklines(pair: Union[str, list[str]], contractType: str, interval: Union[str, list[str]], startTime=None, endTime=None, limit=500, asynchronous=False):
    url = FUTURES_API_URL + '/continuousKlines'
    if not asynchronous:
        if (startTime): startTime = int(startTime * 1000)
        if (endTime) : endTime = int(endTime * 1000)
        params = {
            'pair' : pair,
            'interval' : interval,
            'contractType' : contractType,
            'startTime' : startTime,
            'endTime' : endTime,
            'limit' : limit
        }
        response = requests.get(url, params=params).json()
        return response
    else:
        ret = []
        # Asynchronous API call
        async def get_klines(pairs, intervals, contractType, startTime, endTime, limit):
            async with aiohttp.ClientSession(trust_env=True) as session:
                tasks = []
                for pair in pairs:
                    for interval in intervals:
                        if (startTime): startTime = int(startTime * 1000)
                        if (endTime) : endTime = int(endTime * 1000)
                        params = {
                            'pair' : pair,
                            'interval' : interval,
                            'contractType' : contractType,
                            'startTime' : startTime,
                            'endTime' : endTime,
                            'limit' : limit
                        }
                        URL = url + '?' + urlencode(params)
                        tasks.append(asyncio.create_task(session.get(URL, ssl=False)))
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    ret.append(await response.json())
            return ret
        return asyncio.run(get_klines(pair, interval, contractType, startTime, endTime, limit))

# %%
def futures_price_ticker(symbol: Union[None, str, list[str]]) -> Union[dict, list[dict]]:
    url = FUTURES_API_URL + '/ticker/price'
    if isinstance(symbol, str):
        return requests.get(url = url + '?symbol=' + symbol)
    elif symbol == None:
        return requests.get(url = url)
    else:
        response = requests.get(url=url)
        ret = []
        for asset in response:
            if (asset['symbol'] in symbol):
                ret.append(asset)
        return ret

#%%
def futures_open_interest(symbol: Union[str, list[str]]) -> Union[dict, list[dict]]:
    url = FUTURES_API_URL + '/openInterest'
    if isinstance(symbol, str):
        return requests.get(url + '?symbol=' + symbol)
    else:
        ret = []
        async def get_open_interest(symbols):
            async with aiohttp.ClientSession(trust_env=True) as session:
                tasks = []
                for symbol in symbols:
                    URL = url + '?symbol=' + symbol
                    tasks.append(asyncio.create_task(session.get(URL, ssl=False)))
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    ret.append(await response.json())
            return ret
        return asyncio.run(get_open_interest(symbol))

# %%
def futures_open_interest_statistics(symbol: Union[str, list[str]], period: str, startTime=None, endTime=None, limit=30, asynchronous=False) -> Union[list[list], list[list[list]]]:
    url = 'https://fapi.binance.com/futures/data/openInterestHist'
    if not asynchronous:
        if (startTime): startTime = int(startTime * 1000)
        if (endTime) : endTime = int(endTime * 1000)
        params = {
            'symbol' : symbol,
            'period' : period,
            'startTime' : startTime,
            'endTime' : endTime,
            'limit' : limit
        }
        response = requests.get(url, params=params).json()
        return response
    else:
        ret = []
        # Asynchronous API call
        async def get_klines(symbols, periods, startTime, endTime, limit):
            async with aiohttp.ClientSession(trust_env=True) as session:
                tasks = []
                for symbol in symbols:
                    for period in periods:
                        if (startTime): startTime = int(startTime * 1000)
                        if (endTime) : endTime = int(endTime * 1000)
                        params = {
                            'symbol' : symbol,
                            'period' : period,
                            'startTime' : startTime,
                            'endTime' : endTime,
                            'limit' : limit
                        }
                        URL = url + '?' + urlencode(params)
                        tasks.append(asyncio.create_task(session.get(URL, ssl=False)))
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    ret.append(await response.json())
            return ret
        return asyncio.run(get_klines(symbol, period, startTime, endTime, limit))

#%%
def futures_exchange_information(type : Union[str('SYMBOL'), None]) -> Union[list, dict]:
    url = FUTURES_API_URL + '/exchangeInfo'
    response = requests.get(url).json()
    if type == 'SYMBOL':
        ret = []
        for pos in response['symbols']:
            ret.append(pos['symbol'])
        return ret
    else: return response

# %%
def futures_long_short_ratio(symbol: Union[str, list[str]], period: str, limit=30, asynchronous=False) -> Union[list[list], list[list[list]]]:
    url = 'https://fapi.binance.com/futures/data/globalLongShortAccountRatio'
    if not asynchronous:
        params = {
            'symbol' : symbol,
            'period' : period,
            'limit' : limit
        }
        response = requests.get(url, params=params).json()
        ret = []
        for item in response:
            ret.append([item['timestamp'], item['longShortRatio']])
        return ret
    else:
        ret = []
        def to_list(response):
            res = []
            for item in response:
                res.append([item['timestamp'], item['longShortRatio']])
            return res
        # Asynchronous API call
        async def get_klines(symbols, periods, limit):
            async with aiohttp.ClientSession(trust_env=True) as session:
                tasks = []
                for symbol in symbols:
                    for period in periods:
                        params = {
                            'symbol' : symbol,
                            'period' : period,
                            'limit' : limit
                        }
                        URL = url + '?' + urlencode(params)
                        tasks.append(asyncio.create_task(session.get(URL, ssl=False)))
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    ret.append(to_list(await response.json()))
            return ret
        return asyncio.run(get_klines(symbol, period, limit))
