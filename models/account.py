from abc import ABC, abstractmethod
from exceptions import BankingException


class BankAccount(ABC):
    def __init__(self, account_number: str, initial_balance: float = 0.0):
        self.__account_number = account_number
        self.__balance = 0.0
        if initial_balance > 0:
            self.deposit(initial_balance)

    @property
    def account_number(self):
        return self.__account_number

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise BankingException("Amount must be positive.", "AMOUNT_ERROR")
        self.__balance += amount
        return self.__balance

    def _deduct(self, amount: float):
        self.__balance -= amount

    @abstractmethod
    def withdraw(self, amount: float):
        pass

    @abstractmethod
    def month_end_process(self):
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] Acct#{self.__account_number} | Balance: {self.__balance:,.2f}"

    def __eq__(self, other):
        return isinstance(other, BankAccount) and self.__account_number == other.account_number


class SavingsAccount(BankAccount):
    INTEREST_RATE = 0.02
    MINIMUM_BALANCE = 1000.0

    def withdraw(self, amount: float):
        if amount <= 0:
            raise BankingException("Amount must be positive.", "AMOUNT_ERROR")
        if (self.balance - amount) < self.MINIMUM_BALANCE:
            raise BankingException("Withdrawal breaches minimum balance.", "BALANCE_ERROR")
        self._deduct(amount)
        return self.balance

    def month_end_process(self):
        interest = self.balance * self.INTEREST_RATE
        self.deposit(interest)
        return interest


class CheckingAccount(BankAccount):
    WITHDRAWAL_FEE = 15.0
    OVERDRAFT_LIMIT = -500.0

    def withdraw(self, amount: float):
        if amount <= 0:
            raise BankingException("Amount must be positive.", "AMOUNT_ERROR")
        total = amount + self.WITHDRAWAL_FEE
        if (self.balance - total) < self.OVERDRAFT_LIMIT:
            raise BankingException("Overdraft limit exceeded.", "BALANCE_ERROR")
        self._deduct(total)
        return self.balance

    def month_end_process(self):
        pass


class BusinessAccount(BankAccount):
    MINIMUM_BALANCE = 5000.0
    SERVICE_CHARGE = 250.0

    def withdraw(self, amount: float):
        if amount <= 0:
            raise BankingException("Amount must be positive.", "AMOUNT_ERROR")
        if (self.balance - amount) < self.MINIMUM_BALANCE:
            raise BankingException("Business accounts must maintain minimum balance.", "BALANCE_ERROR")
        self._deduct(amount)
        return self.balance

    def month_end_process(self):
        if self.balance < self.MINIMUM_BALANCE:
            self._deduct(self.SERVICE_CHARGE)
