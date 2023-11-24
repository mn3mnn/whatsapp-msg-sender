import time

from constant import SENT, TIMEOUT, FAILED
from db import *
from account import Account
from urls import *
from response import send_status_response_to_user
from threading import Thread, Event

from redis_conn import pop_msg_from_queue


class Manager:
    def __init__(self):
        self.accounts = []
        self.messages_queue = []
        self.pending_messages = []
        self.thread = None
        self.stop_event = Event()  # Event to stop the thread

    def add_account(self, phone_num):
        AccountDB.add_account(phone_num)
        self.accounts.append(Account(phone_num))
        print(f'added account {phone_num}')
        return True

    def append_msg_to_queue(self, msg: Message):
        self.messages_queue.append(msg)

    def wait_for_new_msgs_in_q_and_append_to_acc_q(self):
        while not self.stop_event.is_set():
            try:
                for i in range(len(self.accounts)):
                    if self.accounts[i].is_logged_in() and self.accounts[i].is_enabled():
                        print(f'account {self.accounts[i]} is logged in and enabled')
                        msg = pop_msg_from_queue()
                        print(f'got msg {msg} from queue')
                        if msg:
                            print(f'appending msg {msg} to account {self.accounts[i]}')
                            self.accounts[i].append_msg_to_queue(msg)
                    else:
                        continue
            except Exception as e:
                print(e)
                continue

    def run(self):
        self.thread = Thread(target=self.wait_for_new_msgs_in_q_and_append_to_acc_q)
        self.thread.start()

    def stop(self):
        self.stop_event.set()  # Set the event to stop the thread
        self.thread.join()

    def __del__(self):
        self.keep_running = False
        self.thread.join()

    def disable_account(self, phone_num):
        for account in self.accounts:
            if account.phone_number == phone_num:
                account.disable()
                break

    def enable_account(self, phone_num):
        for account in self.accounts:
            if account.phone_number == phone_num:
                account.enable()
                break


manager_ = None


def get_manager():
    global manager_
    if manager_ is None:
        manager_ = Manager()
        print('manager created')

    return manager_

