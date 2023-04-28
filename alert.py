import websocket
import json
import time
import requests
import re
from config import *
from datetime import datetime
from typing import Literal, Union

def telegram_bot_sendtext(text : str) -> json:
    pattern = r'([\[\]{}()*+?.\\^$|])'
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

def messenger_bot_sendtext(text : str, recipient_id : int) -> json:
    message_url = f"https://graph.facebook.com/v16.0/me/messages?access_token={MESSENGER_PAGE_SECRET}"
    data = {
        "message" : {
            "text" : text
        },
        "recipient" : {
            "id" : recipient_id
        }
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
    except:
        pass