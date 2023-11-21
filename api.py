import os

from urllib.parse import unquote  # Import the unquote function for URL decoding

from flask import Flask, request, jsonify
from db import Message
from urls import *

API_KEYS = ['123456']

app = Flask(__name__)


@app.route(SEND_MSG_ROUTE, methods=['POST', 'GET'])
def send_message():
    msg_json = {
        'ID': None,
        'attachments': None,
        'deliveredDate': None,
        'deviceID': None,
        'errorCode': None,
        'expiryDate': None,
        'groupID': None,
        'message': None,
        'number': None,
        'prioritize': None,
        'resultCode': None,
        'retries': None,
        'schedule': None,
        'sentDate': None,
        'simSlot': None,
        'status': None,
        'type': None,
        'userID': None
    }

    response_json = {
        'data': {
            'messages': []
        },
        'error': None,
        'success': True
    }

    try:
        data = request.json
        message = data.get('message', None)
        mobile_number = data.get('number', None)
        key = data.get('key', None)
        devices = data.get('devices', None)
        msg_type = data.get('type', None)
        prioritize = data.get('prioritize', None)

        if not all([message, mobile_number, key]):
            response_json['error'] = 'Invalid request'
            response_json['success'] = False
            return jsonify(response_json), 400

        if key not in API_KEYS:
            response_json['error'] = 'Unauthorized'
            response_json['success'] = False
            return jsonify(response_json), 401

        # Check if the message contains URL-encoded links and decode them
        while '%' in message:
            parts = message.split('%', 1)
            non_encoded_part = parts[0]
            encoded_part = parts[1][:2]  # Take the first two characters representing the encoded part
            url_encoded_part = parts[1][2:]  # Take the rest of the encoded part
            # Decode the URL-encoded part
            decoded_url_part = unquote(encoded_part) + url_encoded_part
            # Combine non-encoded part and decoded URL part
            message = non_encoded_part + decoded_url_part

        try:  # Insert message into the database
            msg = Message.add_new_message(message, mobile_number)

            msg_json['ID'] = msg.id
            msg_json['message'] = msg.content
            msg_json['number'] = msg.mobile_number
            msg_json['status'] = msg.status
            msg_json['type'] = 'sms'

            response_json['data']['messages'].append(msg_json.copy())  # Appending a copy of the msg_json

            return jsonify(response_json), 200

        except Exception as e:
            response_json['error'] = "db error, couldn't send the message"
            response_json['success'] = False
            return jsonify(response_json), 500

    except Exception as e:
        response_json['error'] = "Server error, couldn't send the message"
        response_json['success'] = False
        return jsonify(response_json), 500


if __name__ == '__main__':
    app.run(debug=True)  # port=5000

