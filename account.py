import time
from threading import Thread

from db import *
from messanger import Messanger
from response import send_status_response_to_user


class Account(Thread):
    def __init__(self, phone_number, name=None):
        super().__init__(name)
        self.phone_number = phone_number
        self.name = name or phone_number

        self.keep_running = True
        self.msgs_queue = []

        self.messanger = Messanger()

        self.start()  # start the thread

    def run(self):  # this method will be called when the thread starts
        self.__login()
        while self.keep_running:
            if not self.is_logged_in():
                self.__login()

            if self.msgs_queue:
                msg = self.msgs_queue.pop(0)

                status = self.__send_msg(msg)
                if status == "sent":
                    msg.status = "sent"
                    msg.sent_at = datetime.now()
                    msg.save()
                elif status == "failed" or status == "timeout":
                    msg.status = status
                    msg.save()

                send_status_response_to_user(msg)

            else:
                time.sleep(0.5)

    def __str__(self):
        return f"Account: {self.name} ({self.phone_number})"

    def __del__(self):
        pass

    def __login(self):
        return self.messanger.login()

    def is_logged_in(self):
        return self.messanger.is_logged_in()

    def append_msg_to_queue(self, msg: Message):
        self.msgs_queue.append(msg)

    def __send_msg(self, msg: Message):
        return self.messanger.send_message(msg.mobile_number, msg.content)

    def quit(self):
        self.keep_running = False
        self.messanger.driver.quit()
        self.join()

    def disable(self):
        self.keep_running = False

    def enable(self):
        self.keep_running = True






