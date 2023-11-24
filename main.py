from threading import Thread
# from api import app
from manager import get_manager

manager = get_manager()


def main():

    for i in range(1):
        try:
            mobile_number = str(input(f"Enter mobile number of account {i+1}: "))
            manager.add_account(mobile_number)
        except Exception as e:
            print(e)
            print("Try again")
            i -= 1

    manager.run()
    # app.run(debug=True)  # port=5000


if __name__ == "__main__":
    main()
