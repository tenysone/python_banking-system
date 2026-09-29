import math
from abc import ABC, abstractmethod

from exceptions import BankingException


class BankAccount(ABC):
    ACCOUNT_TYPE = "General"
    MINIMUM_BALANCE = 0.0

    def __init__(self, account_number: str, customer_id: str):
        self.__account_number = account_number
        self.__customer_id = customer_id
        self.__balance = 0.0

    # Tinatanggihan ang zero, negative, nan at inf bago magbago ang balance
    @staticmethod
    def _validate_amount(amount: float):
        if amount <= 0:
            raise BankingException("Amount must be a valid number greater than zero.", "INVALID AMOUNT")

    #Changer lang to sa private data (balance)
    def _credit(self, amount: float):
        self._validate_amount(amount)
        self.__balance += amount


    def _debit(self, amount: float, check_limit: bool = True):
        self._validate_amount(amount)
        if check_limit and self.__balance - amount < self._withdrawal_limit():
            raise BankingException(f"Balance cannot go below ₱{self._withdrawal_limit():,.2f}", "INSUFFICIENT BALANCE")
        self.__balance -= amount


    def _withdrawal_limit(self):
        return 0.0

    def deposit(self, amount: float):
        self._credit(amount)

    # Float - ibinabalik ang kabuuang nabawas sa balance (kasama ang fee kung meron)
    @abstractmethod
    def withdraw(self, amount: float):
        pass

    @abstractmethod
    def month_end_process(self):
        pass

    # String - paliwanag ng rules ng bawat account type
    @abstractmethod
    def rules(self):
        pass


    # Atomic: either buo yung transfer or walang nagbago sa dalawang account
    def transfer_to(self, target, amount: float):
        if target is self:
            raise BankingException("Cannot transfer to the same account.", "TRANSFER")
        # Step 1: bawas muna sa source (mag e-error agad kung kulang, wala pang nagbabago)
        self._debit(amount)
        # Step 2: dagdag sa target, kung pumalya ibabalik sa source at ipapasa ang error
        try:
            target.deposit(amount)
        except BankingException:
            self._credit(amount)
            raise

    # bool
    def is_below_minimum(self):
        return self.__balance < self.MINIMUM_BALANCE

    @property
    def account_number(self):
        return self.__account_number

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def account_type(self):
        return self.ACCOUNT_TYPE

    @property
    def balance(self):
        return self.__balance

    def __str__(self):
        return f"{self.__account_number} | {self.ACCOUNT_TYPE} | ₱{self.__balance:,.2f}"

    # Para magamit sa sorted() - mas maliit na balance, mauuna
    def __lt__(self, other):
        return self.balance < other.balance


class SavingsAccount(BankAccount):
    ACCOUNT_TYPE = "Savings"
    MINIMUM_BALANCE = 1000.0
    INTEREST_RATE = 0.02

    # Bawal bumaba sa minimum balance
    def _withdrawal_limit(self):
        return self.MINIMUM_BALANCE

    def withdraw(self, amount: float):
        self._debit(amount)
        return amount

    # May interest kada month end
    def month_end_process(self):
        interest = round(self.balance * self.INTEREST_RATE, 2)
        if interest <= 0:
            return None
        self._credit(interest)
        return ("INTEREST", interest)

    def rules(self):
        return (f"Minimum balance ₱{self.MINIMUM_BALANCE:,.2f}; "
                f"{self.INTEREST_RATE:.0%} interest at month end")

class CheckingAccount(BankAccount):
    ACCOUNT_TYPE = "Checking"
    WITHDRAWAL_FEE = 15.0
    OVERDRAFT_LIMIT = -500.0
    OVERDRAFT_FEE = 50.0

    # Pwede mag negative hanggang overdraft limit
    def _withdrawal_limit(self):
        return self.OVERDRAFT_LIMIT

    # May fee kada withdraw - ibinabalik ang kabuuang nabawas (amount + fee)
    def withdraw(self, amount: float):
        self._validate_amount(amount)
        total = amount + self.WITHDRAWAL_FEE
        self._debit(total)
        return total

    # May overdraft fee kapag negative ang balance sa month end
    def month_end_process(self):
        if self.balance >= 0:
            return None
        self._debit(self.OVERDRAFT_FEE, check_limit=False)
        return ("OVERDRAFT FEE", self.OVERDRAFT_FEE)

    def rules(self):
        return (f"₱{self.WITHDRAWAL_FEE:,.2f} fee per withdrawal; "
                f"overdraft up to ₱{-self.OVERDRAFT_LIMIT:,.2f}; "
                f"₱{self.OVERDRAFT_FEE:,.2f} fee if negative at month end")



class BusinessAccount(BankAccount):
    ACCOUNT_TYPE = "Business"
    MINIMUM_BALANCE = 5000.0
    SERVICE_CHARGE = 250.0

    def withdraw(self, amount: float):
        self._debit(amount)
        return amount

    # May service charge pag below minimum balance
    def month_end_process(self):
        if not self.is_below_minimum():
            return None
        self._debit(self.SERVICE_CHARGE, check_limit=False)
        return ("SERVICE CHARGE", self.SERVICE_CHARGE)

    def rules(self):
        return (f"Minimum balance ₱{self.MINIMUM_BALANCE:,.2f}; "
                f"₱{self.SERVICE_CHARGE:,.2f} service charge if below minimum at month end")