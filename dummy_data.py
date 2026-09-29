from models.customer import Customer
from models.account import SavingsAccount, CheckingAccount, BusinessAccount


# Prepared records para sa demo: 5 customers + 7 accounts + sample transactions
def load_dummy_data(manager):
    manager.add_customer(Customer("C-100001", "Juan Dela Cruz"))
    manager.add_customer(Customer("C-100002", "Maria Santos"))
    manager.add_customer(Customer("C-100003", "Pedro Reyes"))
    manager.add_customer(Customer("C-100004", "Ana Garcia"))
    manager.add_customer(Customer("C-100005", "Jose Mendoza"))

    manager.open_account(SavingsAccount("SA-200001", "C-100001"), 15000)
    manager.open_account(CheckingAccount("CA-200002", "C-100001"), 5000)
    manager.open_account(SavingsAccount("SA-200003", "C-100002"), 8000)
    manager.open_account(BusinessAccount("BA-200004", "C-100003"), 50000)
    manager.open_account(CheckingAccount("CA-200005", "C-100004"), 2000)
    manager.open_account(BusinessAccount("BA-200006", "C-100005"), 6000)
    manager.open_account(SavingsAccount("SA-200007", "C-100005"), 3000)

    manager.deposit("SA-200003", 2000)
    manager.withdraw("SA-200001", 1500)
    manager.withdraw("CA-200005", 2300)
    manager.withdraw("BA-200006", 2500)
    manager.transfer("BA-200004", "CA-200002", 4000)
