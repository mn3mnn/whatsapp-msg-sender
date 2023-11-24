# send post requests to test the api

import requests
from urls import *

from constant import API_KEYS

# send_msg_url = f'http://185.182.184.191' + SEND_MSG_ROUTE
send_msg_url = f'http://127.0.0.1:5000' + SEND_MSG_ROUTE


for i in range(2):
    data = {
        'key': API_KEYS[0],
        'message': f'hello here is a link https://facebook.com/  testNum: {i}',
        'number': '201122960525',
        'type': 'whatsapp'
    }
    response = requests.post(send_msg_url, json=data)
    print(response.status_code)
    print(response.text)
    print()
