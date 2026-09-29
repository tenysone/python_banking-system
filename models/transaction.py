

# Relationship class - may hawak na reference sa mismong account objects
class Transaction():
    def __init__(self, ref: str, type: str, amount: float, source_account, target_account, status: str):
        self.__ref = ref
        self.__type = type
        self.__amount = amount
        self.__source_account = source_account  # account object kung saan galing (None kung deposit)
        self.__target_account = target_account  # account object kung saan papunta (None kung withdraw)
        self.__status = status
        # Resulting balances pagkatapos ng transaction
        self.__source_balance = source_account.balance if source_account else None
        self.__target_balance = target_account.balance if target_account else None

    #String
    @property
    def ref(self):
        return self.__ref

    #String - DEPOSIT, WITHDRAW, TRANSFER, INTEREST, SERVICE CHARGE, OVERDRAFT FEE
    @property
    def type(self):
        return self.__type

    #Float
    @property
    def amount(self):
        return self.__amount

    #String - account number ng source (None kung wala)
    @property
    def source(self):
        return self.__source_account.account_number if self.__source_account else None

    #String - account number ng target (None kung wala)
    @property
    def target(self):
        return self.__target_account.account_number if self.__target_account else None

    #String - SUCCESS or FAILED
    @property
    def status(self):
        return self.__status

    #Float - balance ng isang account pagkatapos ng transaction na ito
    def balance_for(self, account_number: str):
        if account_number == self.source:
            return self.__source_balance
        if account_number == self.target:
            return self.__target_balance
        return None

    #Bool
    def is_success(self):
        return self.__status == "SUCCESS"

    #Bool - kasali ba ang account na ito (source o target) sa transaction
    def involves(self, account_number: str):
        return account_number in (self.source, self.target)


    def __str__(self):
        return f"{self.__ref} | {self.__type} | ₱{self.__amount:,.2f} | {self.__status}"
