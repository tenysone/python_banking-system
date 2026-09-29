from exceptions import BankingException
from manager.bank_manager import BankManager
from dummy_data import load_dummy_data
from models.account import SavingsAccount, CheckingAccount, BusinessAccount
from models.customer import Customer

manager = BankManager()
ACCOUNT_TYPES = {
    "1": ("SA-", SavingsAccount),
    "2": ("CA-", CheckingAccount),
    "3": ("BA-", BusinessAccount),
}

#Display Formater
def peso(amount: float):
    if amount < 0:
        return f"-₱{-amount:,.2f}"
    return f"₱{amount:,.2f}"

def print_result(title: str, account, amount: float, balance_before: float, target=None, fee: float = 0.0):
    print("\n========================================")
    print(f" {title}")
    print("========================================")
    print(f"Account        : {account.account_number} ({account.account_type})")
    if target:
        print(f"To Account     : {target.account_number} ({target.account_type})")
    print(f"Amount         : {peso(amount)}")
    if fee > 0:
        print(f"Fee            : {peso(fee)}")
    print(f"Balance Before : {peso(balance_before)}")
    print(f"Balance After  : {peso(account.balance)}")
    print("========================================\n")

def validate_amount(amount_input: str):
    if amount_input.strip() == "":
        print("##### Please enter an amount")
        return None
    try:
        amount = float(amount_input)
    except ValueError:
        print("##### Only numbers are accepted in this stage")
        return None
    else:
        if amount <= 0:
            print("##### Please enter an amount greater than zero")
            return None
        return amount

def ask_account(label: str):
    while True:
        account_number = input(f"{label} [Press ENTER to go back]: ").strip().upper()
        if account_number == "":
            return None
        try:
            return manager.get_account(account_number)
        except BankingException as error:
            print(f"##### {error}")

def ask_amount(label: str):
    while True:
        amount = validate_amount(input(f"{label} : "))
        if amount is not None:
            return amount

def create_customer():
    print("--------------------------------------------------")
    print("================ Add Customer ====================")
    generated_id = manager.generate_customer_id()
    while True:
        customer_id = input(f"Customer ID [Press ENTER to use {generated_id}]: ").strip()
        if customer_id == "":
            customer_id = generated_id
            print(f"##### The {generated_id} (AUTO GENERATED) will be used.")
            break
        elif not customer_id.isdigit():
            print("##### Please enter only numeric characters only.")
        elif len(customer_id) != 6:
            print("##### Please enter 6 numeric characters only.")
        elif manager.has_customer("C-" + customer_id):
            print(f"##### The ID C-{customer_id} is already taken.")
        else:
            customer_id = "C-" + customer_id
            print(f"===== The ID is set to {customer_id}")
            break

    while True:
        customer_name = input("Customer Name  : ").strip()
        if customer_name == "":
            print("##### Please enter your name.")
        elif any(char.isdigit() for char in customer_name):
            print("##### Name cannot contain numeric characters.")
        else:
            print(f"===== The Name is set to {customer_name}")
            break

    try:
        customer = Customer(customer_id, customer_name)
        manager.add_customer(customer)
    except BankingException as error:
        print(f"##### Failed: {error}")
    else:
        print(f"===== Successfully Added: {customer}")

def open_account():
    print("--------------------------------------------------")
    print("================ Open Account ====================")

    while True:
        customer_id = input("Customer ID [Press ENTER to go back]: ").strip().upper()
        if customer_id == "":
            return
        try:
            manager.get_customer(customer_id)
        except BankingException as error:
            print(f"##### {error}")
            continue

        print("Account type    : [1] Savings  [2] Checking  [3] Business")
        choice = input("Select Type of Account : ").strip()
        if choice not in ACCOUNT_TYPES:
            print("##### Invalid selection. Please select 1-3.")
            continue
        prefix, account_class = ACCOUNT_TYPES[choice]

        generated_id = manager.generate_account_number(prefix)
        account_number = input(f"Account Number [Press ENTER to use {generated_id}]: ").strip().upper()
        if account_number == "":
            account_number = generated_id

        try:
            initial_deposit = float(input(f"Initial deposit (minimum {peso(account_class.MINIMUM_BALANCE)}) : "))
        except ValueError:
            print("##### Invalid amount. Please enter a valid number.")
            continue

        account = account_class(account_number, customer_id)
        try:
            manager.open_account(account, initial_deposit)
        except BankingException as error:
            print(f"##### Failed to open account: {error}")
            continue

        print("\n========================================")
        print(" ACCOUNT SUCCESSFULLY CREATED")
        print("========================================")
        print(f"Customer ID    : {customer_id}")
        print(f"Account ID     : {account.account_number}")
        print(f"Account Type   : {account.account_type}")
        print(f"Rules          : {account.rules()}")
        print(f"Opening Balance: {peso(account.balance)}")
        print("========================================\n")
        return

def deposit():
    print("--------------------------------------------------")
    print("=================== Deposit ======================")
    account = ask_account("Account ID")
    if not account:
        return
    print(f"===== Current Balance: {peso(account.balance)}")
    amount = ask_amount("Deposit amount")

    balance_before = account.balance
    try:
        manager.deposit(account.account_number, amount)
    except BankingException as error:
        print(f"##### Deposit failed: {error}")
    else:
        print_result("DEPOSIT SUCCESSFUL", account, amount, balance_before)
    finally:
        print("===== Returning to main menu...")

def withdraw():
    print("--------------------------------------------------")
    print("=================== Withdraw =====================")
    account = ask_account("Account ID")
    if not account:
        return
    print(f"===== Current Balance: {peso(account.balance)}")
    print(f"===== Rules: {account.rules()}")
    amount = ask_amount("Withdraw amount")

    balance_before = account.balance
    try:
        transaction = manager.withdraw(account.account_number, amount)
    except BankingException as error:
        print(f"##### Withdrawal failed: {error}")
    else:
        # transaction.amount = amount + fee (Checking lang ang may fee)
        print_result("WITHDRAWAL SUCCESSFUL", account, amount, balance_before, fee=transaction.amount - amount)
    finally:
        print("===== Returning to main menu...")

def transfer():
    print("--------------------------------------------------")
    print("=================== Transfer =====================")
    source = ask_account("From Account ID")
    if not source:
        return
    print(f"===== Current Balance: {peso(source.balance)}")
    target = ask_account("To Account ID")
    if not target:
        return
    amount = ask_amount("Transfer amount")

    balance_before = source.balance
    target_before = target.balance
    try:
        manager.transfer(source.account_number, target.account_number, amount)
    except BankingException as error:
        print(f"##### Transfer failed: {error}")
        print(f"===== No changes made. {source.account_number}: {peso(source.balance)} | "
              f"{target.account_number}: {peso(target.balance)}")
    else:
        print_result("TRANSFER SUCCESSFUL", source, amount, balance_before, target)
        print(f"Receiver Balance: {peso(target_before)} -> {peso(target.balance)}\n")
    finally:
        print("===== Returning to main menu...")

def process_month_end():
    print("--------------------------------------------------")
    print("=============== Process Month End ================")
    transactions = manager.process_month_end()
    for transaction in transactions:
        print(transaction)
    print("===== Returning to main menu...")

def search_account():
    print("--------------------------------------------------")
    print("================ Search Account ==================")
    account = ask_account("Account ID")
    if not account:
        return

    print("\n========================================")
    print(" ACCOUNT FOUND")
    print("========================================")
    print(f"Account Number : {account.account_number}")
    print(f"Customer ID    : {account.customer_id}")
    print(f"Account Type   : {account.account_type}")
    print(f"Balance        : {peso(account.balance)}")
    print(f"Rules          : {account.rules()}")
    print("========================================\n")

def display_statement():
    print("--------------------------------------------------")
    print("=============== Display Statement ================")
    account = ask_account("Account ID")
    if not account:
        return
    account_num = account.account_number
    try:
        transactions = manager.get_statement(account_num)
    except BankingException as error:
        print(f"##### Banking failed: {error}")
        return
    print("\n========================================================")
    print("                    ACCOUNT STATEMENT")
    print("========================================================")
    print(f"{'Account Number':<18}: {account.account_number}") #parang padding :<18
    print(f"{'Customer ID':<18}: {account.customer_id}")
    print(f"{'Account Type':<18}: {account.account_type}")
    print(f"{'Current Balance':<18}: {peso(account.balance)}")
    print("========================================================")
    print("\n---------------------- TRANSACTIONS --------------------")
    print("========================================================")
    if not transactions:
        print("No transactions found.")
    else:
        print(
            f"{'Transaction Ref.':<18} | "
            f"{'Type':<16} | "
            f"{'Amount':>12} | "
            f"{'Status':<10}"
        )
        print("--------------------------------------------------------")
        for transaction in transactions:
            print(
                f"{transaction.ref:<18} | "
                f"{transaction.type:<16} | "
                f"{peso(transaction.amount):>12} | "
                f"{transaction.status:<10}"
            )
    print("========================================================\n")

def generate_reports():
    print("--------------------------------------------------")
    print("================ Generate Reports =================")

    print("1. Balances by Account Type")
    print("2. Total Deposits and Withdrawals")
    print("3. Accounts Below Minimum Balance")
    print("4. Transaction Counts and Amounts")

    choice = input("Report Type [Press ENTER to go back]: ").strip()

    if choice == "":
        return

    try:
        report = manager.generate_reports(int(choice))
    except (ValueError, BankingException) as error:
        print(f"##### {error}")
        return

    report_title = ""

    if choice == "1":
        balance_type_report(report)
    elif choice == "2":
        deposits_withdrawals_report(report)
    elif choice == "3":
        below_minimum_balance_report(report)
    elif choice == "4":
        transaction_counts_report(report)

def balance_type_report(report):
    print("\n========================================")
    print("                Balances by Account Type")
    print("========================================")
    print(f"Savings     : {peso(report["Savings"])}")
    print(f"Checking    : {peso(report["Checking"])}")
    print(f"Business    : {peso(report["Business"])}")
    print("========================================\n")

def deposits_withdrawals_report(report):
    print("\n========================================")
    print(f"          Total Deposits and Withdrawals")
    print("========================================")
    print(f"Total Deposits     : {peso(report["DEPOSIT"])}")
    print(f"Total Withdrawals  : {peso(report["WITHDRAW"])}")
    print("========================================\n")

def below_minimum_balance_report(accounts):
    print("\n==================================================")
    print("           ACCOUNTS BELOW MINIMUM BALANCE")
    print("==================================================")
    print(
        f"{'Account Number':<18}"
        f"{'Type':<12}"
        f"{'Current Balance':>16}"
    )
    print("--------------------------------------------------")
    for account in accounts:
        print(
            f"{account.account_number:<18}"
            f"{account.account_type:<12}"
            f"{peso(account.balance):>16}"
        )
    print("--------------------------------------------------")
    print(f"Total Accounts: {len(accounts)}")
    print("==================================================")

def transaction_counts_report(transactions):
    print("\n========================================================")
    print("                  TRANSACTION SUMMARY")
    print("========================================================")
    print(
        f"{'Transaction Type':<20}"
        f"{'Successful':>12}"
        f"{'Failed':>10}"
        f"{'Amount':>16}"
    )
    print("--------------------------------------------------------")
    total_success = 0
    total_failed = 0
    total_amount = 0.0
    for transaction_type, value in transactions.items():
        print(
            f"{transaction_type:<20}"
            f"{value['count']:>12}"
            f"{value['failed']:>10}"
            f"{peso(value['amount']):>16}"
        )
        total_success += value["count"]
        total_failed += value["failed"]
        total_amount += value["amount"]
    print("--------------------------------------------------------")
    print(
        f"{'Total':<20}"
        f"{total_success:>12}"
        f"{total_failed:>10}"
        f"{peso(total_amount):>16}"
    )
    print("========================================================")

def main():
    load_dummy_data(manager)
    print(f"===== Demo data loaded: {manager}")

    while True:
        print("\n========== MULTI ACCOUNT BANKING SYSTEM ==========")
        print("\n  [1] Create customer")
        print("  [2] Open account")
        print("  [3] Deposit")
        print("  [4] Withdraw")
        print("  [5] Transfer")
        print("  [6] Process month end")
        print("  [7] Search account")
        print("  [8] Display statement")
        print("  [9] Generate reports")
        print("  [10] Exit \n")
        print("--------------------------------------------------")

        try:
            choice = int(input("Enter your choice: "))

            match choice:
                case 1:
                    create_customer()
                case 2:
                    open_account()
                case 3:
                    deposit()
                case 4:
                    withdraw()
                case 5:
                    transfer()
                case 6:
                    process_month_end()
                case 7:
                    search_account()
                case 8:
                    display_statement()
                case 9:
                    generate_reports()
                case 10:
                    break
                case _:
                    print("##### Invalid choice. Please select a number between 1 and 10.")

        except ValueError:
            print("##### Please select a number between 1 and 10.")
        except BankingException as error:
            print(f"##### {error}")


if __name__ == "__main__":
    main()
