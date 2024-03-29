import time
from threading import Thread
from datetime import datetime
import logging

from db import db, Message
from messanger import Messanger
from constant import SENT, FAILED, TIMEOUT
from response import send_status_response_to_user


# Configure logging
log_file_path = 'msgs_status.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z')


DEFAULT_TIMEOUT_WAITING = 30


class Account(Thread):
    def __init__(self, phone_number, name=None, timeout_waiting=None):
        super().__init__(name)
        self.phone_number = phone_number
        self.name = name or phone_number
        self.timeout_waiting = timeout_waiting or DEFAULT_TIMEOUT_WAITING

        self.accepting_msgs = True
        self.msgs_queue = []

        self.messanger = Messanger(timeout_waiting=self.timeout_waiting, tab_name=self.name)

        self.start()  # start the thread

    def run(self):  # this method will be called when the thread starts
        while self.accepting_msgs:
            while not self.is_logged_in():
                self.login()

            if self.msgs_queue:
                print('popping msg from acc queue')
                msg = self.msgs_queue.pop(0)

                try:
                    print(f"sending message to {msg.mobile_number} from {self.name} ({self.phone_number})")
                    logging.info(f'\nSending message to {msg.mobile_number} from {self.name} ({self.phone_number})\n')
                except:
                    pass

                status = self.send_msg(msg)

                with db.atomic():
                    if status == SENT:
                        msg.sent_at = datetime.utcnow()
                    elif status == FAILED or status == TIMEOUT:
                        pass

                    msg.status = status
                    msg.save()

                print(f"message {msg},  status: {status}")

                send_status_response_to_user(msg)

            else:
                time.sleep(0.1)

    def __str__(self):
        return f"Account: {self.name} ({self.phone_number})"

    def __del__(self):
        try:
            self.messanger.driver.quit()
        except:
            pass
        try:
            db.close()
        except:
            pass

    def login(self):  # open whatsapp web and wait until the qr code is scanned
        self.messanger.login()

    def is_logged_in(self):
        return self.messanger.is_logged_in()

    def append_msg_to_queue(self, msg: Message):
        self.msgs_queue.append(msg)

    def send_msg(self, msg: Message):  # send message and return status
        return self.messanger.send_message(msg.mobile_number, msg.content)

    def quit(self):
        self.accepting_msgs = False
        self.messanger.driver.quit()
        self.join()

    def disable(self):  # disable account from sending messages
        self.accepting_msgs = False

    def enable(self):  # enable account to send messages
        self.accepting_msgs = True

    def is_enabled(self):  # check if account is enabled to send messages
        return self.accepting_msgs





