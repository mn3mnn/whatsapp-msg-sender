import redis
import pickle
# from db import Message


# Connect to a local Redis server
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def append_msg_to_queue(msg):  # msg is a Message object
    try:
        msg = pickle.dumps(msg)
        redis_conn.rpush('messages_queue', msg)
        print(f'Appended msg {msg} to messages_queue')
        return True
    except Exception as e:
        print(e)
        return False


def pop_msg_from_queue():
    try:
        msg = redis_conn.lpop('messages_queue')
        if msg:
            msg = pickle.loads(msg)  # msg is a Message object
            print(f'Got msg {msg} from messages_queue')
            return msg
        else:
            return None

    except Exception as e:
        print(e)
        return None
