import sys
from manager import get_manager

manager = get_manager()


def main():
    timeout = int(input("enter waiting timeout for each message status (in seconds)"))
    n_accounts = int(input("enter num of accounts to add:"))
    for i in range(n_accounts):
        try:
            mobile_number = str(input(f"Enter mobile number of account {i+1}: "))
            manager.add_account(mobile_number, timeout)
        except Exception as e:
            print(e)
            print("Try again")
            i -= 1

    manager.run()


if __name__ == "__main__":
    main()
