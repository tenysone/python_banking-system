from manager.bank_manager import BankManager


def main():
    manager = BankManager()

    while True:
        print("\n=== MULTI ACCOUNT BANKING SYSTEM ===")
        print("1. Create Customer")
        print("2. Open Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. Process Month End")
        print("7. Search Account")
        print("8. Display Statement")
        print("9. Generate Reports")
        print("10. Exit")

        try:
            choice = int(input("Select: "))
        except ValueError:
            print("Invalid input.")
            continue

        if choice == 10:
            print("Goodbye.")
            break
        else:
            print("Not yet implemented.")


if __name__ == "__main__":
    main()
