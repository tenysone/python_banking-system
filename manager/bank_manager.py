from exceptions import BankingException
from models.transaction import Transaction


class BankManager:
    def __init__(self):
        self.__customers = {}
        self.__accounts = {}
        self.__transactions = []

    def add_customer(self, customer):
        raise NotImplementedError

    def open_account(self, customer_id: str, account):
        raise NotImplementedError

    def deposit(self, account_number: str, amount: float):
        raise NotImplementedError

    def withdraw(self, account_number: str, amount: float):
        raise NotImplementedError

    def transfer(self, from_num: str, to_num: str, amount: float):
        raise NotImplementedError

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
