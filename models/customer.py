class Customer:
    def __init__(self, customer_id: str, name: str):
        self.__customer_id = customer_id
        self.__name = name
        self.__account_numbers = []

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def name(self):
        return self.__name

    def add_account(self, account_number: str):
        self.__account_numbers.append(account_number)

    def get_accounts(self):
        return list(self.__account_numbers)

    def __str__(self):
        return f"Customer[{self.__customer_id}] {self.__name} | Accounts: {self.__account_numbers}"

    def __len__(self):
        return len(self.__account_numbers)
