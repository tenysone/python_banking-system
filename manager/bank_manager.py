import math
import random

from exceptions import BankingException
from models.transaction import Transaction


class BankManager:
    def __init__(self):
        self.__customers = {}      # customer_id -> Customer
        self.__accounts = {}       # account_number -> BankAccount
        self.__transactions = []   # lahat ng Transaction, naka-order

    # ===================== CUSTOMERS =====================
    def has_customer(self, customer_id: str):
        return customer_id in self.__customers

    def add_customer(self, customer):
        if self.has_customer(customer.customer_id):
            raise BankingException(f"Customer ID {customer.customer_id} already exists.", "DUPLICATE")
        self.__customers[customer.customer_id] = customer

    def get_customer(self, customer_id: str):
        customer = self.__customers.get(customer_id)
        if customer is None:
            raise BankingException(f"Customer {customer_id} does not exist.", "NOT FOUND")
        return customer

    # ===================== ACCOUNTS =====================
    def has_account(self, account_number: str):
        return account_number in self.__accounts

    def get_account(self, account_number: str):
        account = self.__accounts.get(account_number)
        if account is None:
            raise BankingException(f"Account {account_number} does not exist.", "NOT FOUND")
        return account

    def open_account(self, account, initial_deposit: float):
        customer = self.get_customer(account.customer_id)
        if self.has_account(account.account_number):
            raise BankingException(f"Account number {account.account_number} already exists.", "DUPLICATE")
        if not math.isfinite(initial_deposit) or initial_deposit < 0:
            raise BankingException("Initial deposit must be a valid number and cannot be negative.", "INVALID AMOUNT")
        if initial_deposit < account.MINIMUM_BALANCE:
            raise BankingException(f"{account.account_type} account needs at least ₱{account.MINIMUM_BALANCE:,.2f} to open.", "INVALID AMOUNT")

        # Pasado lahat ng check, saka lang i-save
        self.__accounts[account.account_number] = account
        customer.add_account(account.account_number)
        if initial_deposit > 0:
            self.deposit(account.account_number, initial_deposit)

    # ===================== TRANSACTIONS =====================
    def deposit(self, account_number: str, amount: float):
        account = self.get_account(account_number)
        account.deposit(amount)
        return self.__record("DEPOSIT", amount, None, account, "SUCCESS")

    def withdraw(self, account_number: str, amount: float):
        account = self.get_account(account_number)
        try:
            # Kabuuang nabawas (kasama ang withdrawal fee ng Checking)
            deducted = account.withdraw(amount)
        except BankingException:
            self.__record("WITHDRAW", amount, account, None, "FAILED")
            raise
        return self.__record("WITHDRAW", deducted, account, None, "SUCCESS")

    def transfer(self, from_number: str, to_number: str, amount: float):
        # Kukunin muna parehong account, mag e-error agad kung wala (walang nagbago pa)
        source = self.get_account(from_number)
        target = self.get_account(to_number)
        try:
            source.transfer_to(target, amount)
        except BankingException:
            self.__record("TRANSFER", amount, source, target, "FAILED")
            raise
        return self.__record("TRANSFER", amount, source, target, "SUCCESS")

    def __record(self, type: str, amount: float, source, target, status: str):
        ref = f"T-{len(self.__transactions) + 1:05d}"
        transaction = Transaction(ref, type, amount, source, target, status)
        self.__transactions.append(transaction)
        return transaction

    # ===================== NOT YET IMPLEMENTED (6-9) =====================
    def process_month_end(self):
        raise NotImplementedError

    def search_account(self, account_number: str):
        raise NotImplementedError

    def get_statement(self, account_number: str):
        raise NotImplementedError

    def generate_reports(self):
        raise NotImplementedError

    def get_all_accounts(self):
        return self.__accounts

    def get_all_transactions(self):
        return self.__transactions

    # ===================== ID GENERATORS =====================
    def generate_customer_id(self):
        while True:
            generated_id = "C-" + str(random.randint(100000, 999999))
            if not self.has_customer(generated_id):
                return generated_id

    def generate_account_number(self, prefix: str):
        while True:
            generated_id = prefix + str(random.randint(100000, 999999))
            if not self.has_account(generated_id):
                return generated_id

    # ===================== MAGIC METHODS =====================
    # len(manager) = ilang account meron sa bangko
    def __len__(self):
        return len(self.__accounts)

    def __str__(self):
        return (f"BankManager | {len(self.__customers)} customer(s) | "
                f"{len(self.__accounts)} account(s) | {len(self.__transactions)} transaction(s)")
