import datetime
import json
import os

from urllib.parse import unquote  # Import the unquote function for URL decoding

from flask import Flask, request, jsonify
from urls import *
import logging
import uuid

from manager import get_manager
from constant import API_KEYS


app = Flask(__name__)

manager = get_manager()

# Configure logging
log_file_path = 'incoming_requests.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z')


def get_json_response(success=True, error=None, msg=None):
    response_json = {
        'data': {
            'messages': [msg] if msg else []
        },
        'error': error,
        'success': success
    }
    return response_json


def get_msg_json(msg):
    msg_json = {
        'ID': msg.id,
        'attachments': None,
        'deliveredDate': None,
        'deviceID': None,
        'errorCode': None,
        'expiryDate': None,
        'groupID': None,
        'message': msg.content,
        'number': msg.mobile_number,
        'prioritize': None,
        'resultCode': None,
        'retries': None,
        'schedule': None,
        'sentDate': None,
        'simSlot': None,
        'status': msg.status,
        'type': 'whatsapp',
        'userID': None
    }
    return msg_json


#
# while '%' in content and content.index('%') < len(content) - 2:
#     parts = content.split('%', 1)
#     non_encoded_part = parts[0]
#     encoded_part = parts[1][:2]  # Take the first two characters representing the encoded part
#     url_encoded_part = parts[1][2:]  # Take the rest of the encoded part
#     # Decode the URL-encoded part
#     decoded_url_part = unquote(encoded_part) + url_encoded_part
#     # Combine non-encoded part and decoded URL part
#     content = non_encoded_part + decoded_url_part


@app.route(SEND_MSG_ROUTE, methods=['POST', 'GET'])
def send_message():
    try:
        data = request.json
        content = data.get('message', None)
        mobile_number = data.get('number', None)
        key = data.get('key', None)
        devices = data.get('devices', None)
        msg_type = data.get('type', None)
        prioritize = data.get('prioritize', None)

        req_id = str(uuid.uuid4())

        try:
            # Log incoming request
            print(f'\nIncoming request: {datetime.datetime.utcnow()} {request.method} - JSON: {request.json}\n')
            logging.info(f'\nIncoming request: {req_id} {request.method} {request.url} - JSON: {request.json}\n')
        except Exception as e:
            pass

        if not all([content, mobile_number, key]):
            response_json = get_json_response(success=False, error='Invalid request')
            return jsonify(response_json), 400

        if key not in API_KEYS:
            response_json = get_json_response(success=False, error='Unauthorized')
            return jsonify(response_json), 401

        # Check if the message contains URL-encoded links and decode them
        if '%' in content:
            content = unquote(content)

        try:  # Insert message into the database
            msg = manager.save_msg_to_db(content, mobile_number)

            if not msg:
                response_json = get_json_response(success=False, error="db error, couldn't send the message")
                return jsonify(response_json), 500

            manager.append_msg_to_queue(msg)

            msg_json = get_msg_json(msg)
            response_json = get_json_response(msg=msg_json.copy())

            try:  # Log the response that is sent to the client
                logging.info(f'\nResponse: {req_id} {json.dumps(response_json)}\n')
            except Exception as e:
                pass

            return jsonify(response_json), 200

        except Exception as e:
            response_json = get_json_response(success=False, error="db error, couldn't send the message")
            return jsonify(response_json), 500

    except Exception as e:
        response_json = get_json_response(success=False, error="server error, couldn't send the message")
        return jsonify(response_json), 500


if __name__ == '__main__':
    app.run(debug=True)  # port=5000

