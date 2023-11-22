import websocket
import json
import time
import requests
import re, httpx
from config import *
from datetime import datetime
from typing import Literal, Union
import asyncio, aiohttp
from urllib.parse import urlencode
import trace

def telegram_bot_sendtext(text : str) -> dict:
    pattern = r'([\[\]{}()*+?.\\^$|\-\_\!=])'
    text = re.sub(pattern, r'\\\1', text)
    params = {
        'chat_id' : TELEGRAM_CHAT_ID,
        'parse_mode' : "MarkdownV2",
        'text' : text
    }
    url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage?"
    response = requests.get(url, params=params).json()
    if not response.get('ok') or response['ok'] == False:
        f = open('log.txt', 'a+', encoding='utf-8')
        cur = datetime.now()
        f.write(cur.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        f.write(str(response) + '\n')
        f.write('reason: \n')
        f.write(str(params) + '\n\n')
        f.close()
    return response

def telegram_bot_sendtexts(texts : list[str]) -> list[dict]:
    async def send(texts):
        ret = []
        async with aiohttp.ClientSession(trust_env=True) as session:
            tasks = []
            for text in texts:
                pattern = r'([\[\]{}()*+?.\\^$|\-\_\!])'
                text = re.sub(pattern, r'\\\1', text)
                params = {
                    'chat_id' : TELEGRAM_CHAT_ID,
                    'parse_mode' : "MarkdownV2",
                    'text' : text
                }
                url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage?" + urlencode(params)
                tasks.append(asyncio.create_task(session.get(url, ssl=False)))
            responses = await asyncio.gather(*tasks)
            for response in responses:
                ret.append(await response.json())
        return ret
    return asyncio.run(send(texts))

async def messenger_bot_sendtext_async(recipient_id : int, text : str) -> dict:
    client = httpx.AsyncClient()
    message_url = f"https://graph.facebook.com/v16.0/me/messages?access_token={MESSENGER_PAGE_SECRET}"
    data = {
        "message" : {
            "text" : text
        },
        "recipient" : {
            "id" : recipient_id
        },
        "messaging_type" : "MESSAGE_TAG",
        "tag" : "ACCOUNT_UPDATE"
    }
    try:
        if data.get('recipient') and int(data['recipient']['id']) == int(MESSENGER_PAGE_ID):
            return
        content = await client.post(message_url, json = data)
        if 'error' in content.text:
            f = open('log.txt', 'a+', encoding='utf-8')
            cur = datetime.now()
            f.write(cur.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
            f.write(content.text + '\n')
            f.write('reason: \n')
            f.write(str(data) + '\n\n')
            f.close()
        return content.json()
    except Exception as e:
        f = open('log.txt', 'a+', encoding='utf-8')
        cur = datetime.now()
        f.write(cur.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        f.write(str(e) + '\n')
        f.write('reason: \n')
        f.write(str(data) + '\n\n')
        f.close()
        pass

def messenger_bot_sendtext(recipient_id : int, text : str) -> dict:
    message_url = f"https://graph.facebook.com/v16.0/me/messages?access_token={MESSENGER_PAGE_SECRET}"
    data = {
        "message" : {
            "text" : text
        },
        "recipient" : {
            "id" : recipient_id
        },
        "messaging_type" : "MESSAGE_TAG",
        "tag" : "ACCOUNT_UPDATE"
    }
    try:
        if data.get('recipient') and int(data['recipient']['id']) == int(MESSENGER_PAGE_ID):
            return
        content = requests.post(message_url, json = data)
        if 'error' in content.text:
            f = open('log.txt', 'a+', encoding='utf-8')
            cur = datetime.now()
            f.write(cur.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
            f.write(content.text + '\n')
            f.write('reason: \n')
            f.write(str(data) + '\n\n')
            f.close()
        return content.json()
    except Exception as e:
        f = open('log.txt', 'a+', encoding='utf-8')
        cur = datetime.now()
        f.write(cur.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        f.write(str(e) + '\n')
        f.write('reason: \n')
        f.write(str(data) + '\n\n')
        f.close()
        pass