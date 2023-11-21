from db import *
from messanger import Messanger


class Account:
    def __init__(self, phone_number, name=None):
        self.phone_number = phone_number
        self.name = name or phone_number
        self.logged_in = False
        self.msgs_queue = []
        self.messanger = Messanger()

    def __str__(self):
        return f"Account: {self.name} ({self.phone_number})"

    def __del__(self):
        pass

    def login(self):
        return self.messanger.login()

    def send_msg(self, msg, to):
        # self.msgs_queue.append({"msg": msg,
        #                         "to": to})
        pass

