import uuid


class Transaction:
    def __init__(self, tx_type: str, amount: float, source_account, target_account=None):
        self.__ref = str(uuid.uuid4())[:8].upper()
        self.__type = tx_type
        self.__amount = amount
        self.__source = source_account
        self.__target = target_account
        self.__status = "PENDING"
        self.__balance_after = None

    def complete(self, balance_after: float):
        self.__status = "SUCCESS"
        self.__balance_after = balance_after

    def fail(self):
        self.__status = "FAILED"

    @property
    def ref(self):
        return self.__ref

    @property
    def tx_type(self):
        return self.__type

    @property
    def amount(self):
        return self.__amount

    @property
    def status(self):
        return self.__status

    @property
    def source_account(self):
        return self.__source

    @property
    def target_account(self):
        return self.__target

    @property
    def balance_after(self):
        return self.__balance_after

    def __str__(self):
        return (f"TXN#{self.__ref} | {self.__type} | {self.__amount:,.2f} "
                f"| {self.__status} | Balance After: {self.__balance_after}")
