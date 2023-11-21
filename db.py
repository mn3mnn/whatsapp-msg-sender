from dotenv import load_dotenv
from peewee import *
from playhouse.db_url import connect
from os import getenv
from datetime import datetime

load_dotenv()

db = connect(getenv("DATABASE_URL"))


class BaseModel(Model):
    class Meta:
        database = db


class Message(BaseModel):
    id = AutoField(primary_key=True)
    content = TextField(null=False)
    mobile_number = CharField(max_length=20, null=False)
    status = CharField(max_length=45, default="unsent")
    added_at = DateTimeField(default=datetime.utcnow)
    pending_at = DateTimeField(null=True)
    sent_at = DateTimeField(null=True)
    account_mobile_number = CharField(max_length=20, null=True)  # mobile number of the account that sent this message
    # user_id/user_key = TextField(null=True) not null

    def __str__(self):
        return f"Message: {self.content} to {self.mobile_number}"

    @classmethod
    def add_new_message(cls, content, mobile_number):
        msg = cls.create(content=content, mobile_number=mobile_number)
        return msg

    @classmethod
    def get_msg(cls, msg_id):
        return cls.select().where(cls.id == msg_id).get()

    @classmethod
    def get_messages_by_status(cls, status):
        return cls.select().where(cls.status == status)

    @classmethod
    def get_status(cls, msg_id):
        msg = cls.select().where(cls.id == msg_id).get()
        return msg.status

    @classmethod
    def set_msg_status(cls, msg_id, status):
        msg = cls.select().where(cls.id == msg_id).get()
        msg.status = status
        msg.save()

    @classmethod
    def set_msg_pending_at(cls, msg_id, pending_at):
        msg = cls.select().where(cls.id == msg_id).get()
        msg.pending_at = pending_at
        msg.save()

    @classmethod
    def set_msg_sent_at(cls, msg_id, sent_at):
        msg = cls.select().where(cls.id == msg_id).get()
        msg.sent_at = sent_at
        msg.save()

    @classmethod
    def set_msg_account_mobile_number(cls, msg_id, account_mobile_number):
        msg = cls.select().where(cls.id == msg_id).get()
        msg.account_mobile_number = account_mobile_number
        msg.save()


class Account(BaseModel):
    phone_number = CharField(primary_key=True, max_length=20)
    name = CharField(max_length=45, default=f"{phone_number}")

    def __str__(self):
        return f"Account: {self.name} ({self.phone_number})"

    @classmethod
    def add_new_account(cls, phone_number, name=None):
        account = cls.create(phone_number=phone_number, name=name or phone_number)
        return account

    @classmethod
    def get_account(cls, phone_number):
        return cls.select().where(cls.phone_number == phone_number).get()

    @classmethod
    def get_all_accounts(cls):
        return cls.select()

    @classmethod
    def get_n_accounts(cls, n):
        return cls.select().limit(n)



class User(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=45, null=True)
    user_key = CharField(max_length=45, null=False, unique=True)

    def __str__(self):
        return f"User: {self.name} ({self.user_key})"

    @classmethod
    def add_new_user(cls, user_key, name=None):
        user = cls.create(user_key=user_key, name=name)
        return user

    @classmethod
    def get_user(cls, user_key):
        return cls.select().where(cls.user_key == user_key).get()


if __name__ == "__main__":
    db.create_tables([Message])  # create tables if not exists

    # uncomment the below line to add new message to db, then run this file
    # Message.add_new_message("Hello", "0123456789")
