

class Customer:
    def __init__(self, customer_id: str, name: str):
        self.__customer_id = customer_id
        self.__name = name
        self.__accounts = []  # listahan ng account numbers

    def add_account(self, account_number: str):
        self.__accounts.append(account_number)

    # List - kopya lang ang binibigay para hindi mabago sa labas
    def get_accounts(self):
        return list(self.__accounts)

    #String
    @property
    def customer_id(self):
        return self.__customer_id

    #String
    @property
    def customer_name(self):
        return self.__name

    # len(customer) = ilang account meron siya
    def __len__(self):
        return len(self.__accounts)

    def __str__(self):
        return f"{self.__customer_id} | {self.__name} | {len(self)} account(s)"
