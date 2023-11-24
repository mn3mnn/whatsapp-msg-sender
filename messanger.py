import os
import random
import time
import json
import platform
from dotenv import load_dotenv
from urllib.parse import quote  # Uncomment line below to use python 3

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from db import *
from constant import SENT, FAILED, TIMEOUT

load_dotenv()  # take environment variables from example_for_dot_env.


class Messanger:
    def __init__(self, timeout_waiting=40, tab_name=None):
        self.timeout_waiting = timeout_waiting  # timeout waiting for msg status to be sent
        self.tab_name = tab_name  # name of the tab

        firefox_options = Options()
        # firefox_options.set_preference("permissions.default.image", 2)  # 2 means block images

        ff_profile = webdriver.FirefoxProfile('profile')

        if platform.system() == "Linux":
            self.driver = webdriver.Firefox(options=firefox_options)
        elif platform.system() == "Windows":
            geckodriver_path = os.getenv('GECKODRIVER_PATH')
            firefox_binary = os.getenv('FIREFOX_BIN')

            self.driver = webdriver.Firefox(executable_path=geckodriver_path,
                                            firefox_binary=firefox_binary,
                                            options=firefox_options,
                                            firefox_profile=ff_profile)

        self.driver.maximize_window()
        self.wait5 = WebDriverWait(self.driver, 5)
        self.wait10 = WebDriverWait(self.driver, 10)
        self.wait30 = WebDriverWait(self.driver, 20)
        self.wait120 = WebDriverWait(self.driver, 120)

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

    def is_logged_in(self):
        try:
            # Execute JavaScript to get token value from local storage
            script = "return localStorage.getItem('me-display-name');"
            value = self.driver.execute_script(script)
            # value = json.loads(value)
            return value is not None
        except:
            return False

    def login(self):  # open whatsapp web and wait until the qr code is scanned
        try:
            self.driver.get("https://web.whatsapp.com")
            time.sleep(1)

            if self.tab_name:
                # Use JavaScript to set the title of the web page to <tab_name>
                self.driver.execute_script(f"document.title = '## {self.tab_name} ##';")

            while not self.is_logged_in():
                time.sleep(0.5)
            return True

        except Exception as e:
            print(e)
            return False

    def send_message(self, mobile_number, content):
        try:
            message_input_selector = 'footer div[role="textbox"]'
            sent_msg_status_selector = 'span[data-icon="msg-check"]'
            dlvrd_or_read_msg_status_selector = 'span[data-icon="msg-dblcheck"]'

            msg = quote(content)  # url-encode the message

            url = "https://web.whatsapp.com/send?phone=" + mobile_number + "&text=" + msg

            self.driver.get(url)

            try:  # wait until the message input in the chat is loaded
                WebDriverWait(self.driver, self.timeout_waiting)\
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, message_input_selector)))
            except:
                return TIMEOUT

            time.sleep(random.uniform(0, 0.3))  # sleep random time between 0 and 0.3 seconds
            self.driver.find_element(By.CSS_SELECTOR, message_input_selector).send_keys(Keys.ENTER)

            time.sleep(random.uniform(0, 0.5))  # sleep random time between 0 and 0.5 seconds
            msg_element = self.driver.find_elements(By.CSS_SELECTOR, ".message-out")[-1]  # last msg we just sent on the chat

            # wait until msg is sent or delivered and return status
            try:
                WebDriverWait(self.driver, self.timeout_waiting / 2)\
                    .until(lambda driver: driver.find_elements(By.CSS_SELECTOR, sent_msg_status_selector)
                                          or driver.find_elements(By.CSS_SELECTOR, dlvrd_or_read_msg_status_selector))
            except Exception as e:
                print(e)
                return TIMEOUT

            return SENT

            # n_sent_checkmarks = len(self.driver.find_elements(By.CSS_SELECTOR, sent_msg_status_selector))
            # print(n_sent_checkmarks)
            # n_dlvrd_or_read_checkmarks = len(self.driver.find_elements(By.CSS_SELECTOR, dlvrd_or_read_msg_status_selector))
            # print(n_dlvrd_or_read_checkmarks)
            #
            # time.sleep(random.uniform(0, 0.3))  # sleep random time between 0 and 0.3 seconds
            # self.driver.find_element(By.CSS_SELECTOR, message_input_selector).send_keys(Keys.ENTER)
            #
            # # wait until msg is sent and return status
            # try:  # compare num of sent checkmarks and dlvrd checkmarks before and after sending the msg
            #     WebDriverWait(self.driver, 5 + self.timeout_waiting / 3)\
            #         .until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, sent_msg_status_selector)) > n_sent_checkmarks
            #                               or len(driver.find_elements(By.CSS_SELECTOR, dlvrd_or_read_msg_status_selector)) > n_dlvrd_or_read_checkmarks)
            #     return SENT
            # except Exception as e:
            #     print(e)
            #     return TIMEOUT

        except Exception as e:
            print(e)
            return FAILED


if __name__ == "__main__":
    m = Messanger()
    m.login()
    ch = input("Enter 0 to quit or enter the mobile number followed by the msg to sent: ")
    while ch != "0":
        mobile_number, content = ch.split(" ", 1)
        print(m.send_message(mobile_number, content))
        ch = input("Enter 0 to quit or enter the mobile number followed by the msg to sent: ")

