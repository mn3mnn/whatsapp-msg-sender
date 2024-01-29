# whatsapp-msg-sender

Flask API to send WhatsApp messages from pre-added WhatsApp sessions using selenium web driver.

**Steps:**
- modify `.env`
- run `main.py` to add accounts and scan QR codes
- run `api.py` to listen for incoming requests

- Python code to test the API:

  ```
  import requests
  from urls import *

  from constant import API_KEYS
  send_msg_url = f'http://127.0.0.1:5000' + SEND_MSG_ROUTE
  data = {
        'key': API_KEYS[0],
        'message': "test msg",
        'number': "20xxxxxxxxxxx",
        'type': 'whatsapp'
  }
  response = requests.post(send_msg_url, json=data)
  ```
