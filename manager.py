import time
from threading import Thread, Event

from constant import SENT, TIMEOUT, FAILED
from db import db, Message, AccountDB
from account import Account

from redis_conn import pop_msg_from_queue


class Manager:
    def __init__(self):
        self.accounts = []
        self.messages_queue = []
        self.pending_messages = []
        self.thread = None
        self.stop_event = Event()  # Event to stop the thread

    def add_account(self, phone_num, timout_waiting):
        AccountDB.add_account(phone_num)
        self.accounts.append(Account(phone_num, timeout_waiting=timout_waiting))
        print(f'added account {phone_num}')
        return True

    def wait_for_new_msgs_in_q_and_append_to_acc_q(self):
        acc_index = 0
        while not self.stop_event.is_set() and len(self.accounts) > 0:
            try:
                msg = pop_msg_from_queue()
                if msg:
                    while not self.accounts[acc_index].is_logged_in() or not self.accounts[acc_index].is_enabled():
                        acc_index = (acc_index + 1) % len(self.accounts)

                    self.accounts[acc_index].append_msg_to_queue(msg)
                    acc_index = (acc_index + 1) % len(self.accounts)

                    print(f'Appended msg {msg} to account {self.accounts[acc_index].phone_number} queue')

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


if __name__ == '__main__':
    manager_ = get_manager()
    manager_.accounts = [0, 1, 2, 3, 4]
    manager_.wait_for_new_msgs_in_q_and_append_to_acc_q()
