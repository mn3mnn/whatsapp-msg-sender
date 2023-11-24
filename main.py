from threading import Thread

from api import app
import sys
from manager import get_manager


def main():  # args: timeout_waiting and failed (optional)
    # args = sys.argv
    # n_accounts = 1
    # timout_waiting = 15
    #
    # if len(args) > 1:
    #     try:
    #         n_accounts = int(args[1])
    #     except Exception as e:
    #         pass
    #
    # if len(args) > 2:
    #     try:
    #         timout_waiting = int(args[2])
    #     except Exception as e:
    #         pass

    manager = get_manager()

    for i in range(1):
        try:
            mobile_number = str(input(f"Enter mobile number of account {i+1}: "))
            manager.add_account(mobile_number)
        except Exception as e:
            print(e)
            print("Try again")
            i -= 1

    flask_thread = Thread(target=lambda : app.run(debug=True))
    flask_thread.start()

    manager.run()
    # app.run(debug=True)  # port=5000


if __name__ == "__main__":
    main()
