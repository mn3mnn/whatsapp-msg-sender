import json
import requests
import time

from db import Message
from urls import SEND_RESPONSE_URL


# send response to the user who sent the message (to his static api)
def send_status_response_to_user(msg: Message):
    try:
        url = SEND_RESPONSE_URL

        data = {
            "msg_id": msg.id,
            "mobile_number": msg.mobile_number,
            "status": msg.status,
            "added_at": msg.added_at,
            "pending_at": msg.pending_at,
            "sent_at": msg.sent_at
        }

        requests.post(url, data=json.dumps(data))

    except:
        print(f"Failed to send status response for msg:{msg}")
        pass
