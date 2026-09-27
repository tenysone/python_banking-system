import uuid

from exceptions import BankingException
from models.account import SavingsAccount, CheckingAccount, BusinessAccount, BankAccount
from models.customer import Customer
from models.transaction import Transaction


class BankManager:
    def __init__(self):
        self.__customers = {}
        self.__accounts = {}
        self.__transactions = []

    def add_customer(self, customer):
        customer_id = f"C{len(self.__customers) + 1:03d}"
        new_customer = Customer(customer_id, customer)
        self.__customers[customer_id] = new_customer

        return new_customer

    def open_account(self, customer_id: str, account_type, initial_balance: float):
        if customer_id not in self.__customers:
            raise BankingException("Customer not found.", "CUSTOMER_ERROR")

        customer = self.__customers[customer_id]

        new_account = None
        account_number = f"A{len(self.__accounts) + 1:03d}"
        if account_type == "SavingsAccount":
            new_account = SavingsAccount(account_number, initial_balance)
        elif account_type == "CheckingAccount":
            new_account = CheckingAccount(account_number, initial_balance)
        elif account_type == "BusinessAccount":
            new_account = BusinessAccount(account_number, initial_balance)
        if customer_id not in self.__customers:
            raise BankingException("Customer not found.", "CUSTOMER_ERROR")

        self.__accounts[account_number] = new_account
        customer.add_account(account_number)
        return new_account

    def deposit(self, account_number: str, amount: float):
        if account_number not in self.__accounts:
            raise BankingException("Account not found.", "ACCOUNT_ERROR")

        account: BankAccount = self.__accounts[account_number]
        account.deposit(amount)

    def withdraw(self, account_number: str, amount: float):
        if account_number not in self.__accounts:
            raise BankingException("Account not found.", "ACCOUNT_ERROR")

        account: BankAccount = self.__accounts[account_number]
        account.withdraw(amount)

    def transfer(self, from_num: str, to_num: str, amount: float):
        if from_num not in self.__accounts:
            raise BankingException("Source account not found.", "ACCOUNT_ERROR")

        if to_num not in self.__accounts:
            raise BankingException("Target account not found.", "ACCOUNT_ERROR")

        from_account: BankAccount = self.__accounts[from_num]
        to_account: BankAccount = self.__accounts[to_num]

        from_account.withdraw(amount)
        to_account.deposit(amount)
        #handle error in main?


    def process_month_end(self):
        raise NotImplementedError

    def search_account(self, account_number: str):
        raise NotImplementedError

    def get_statement(self, account_number: str):
        raise NotImplementedError

    def generate_reports(self):
        raise NotImplementedError

    def _get_account(self, account_number: str):
        if account_number not in self.__accounts:
            raise BankingException("Account not found.", "ACCOUNT_ERROR")
        return self.__accounts[account_number]

    def get_all_accounts(self):
        return self.__accounts

    def get_all_transactions(self):
        return self.__transactions
