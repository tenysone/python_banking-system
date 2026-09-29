def report_balances_by_type(accounts: dict):
    totals = {"Savings": 0.0, "Checking": 0.0, "Business": 0.0}
    for account in accounts.values():
        totals[account.account_type] = totals.get(account.account_type, 0.0) + account.balance
    return totals

def report_total_deposits_withdrawals(transactions: list):
    successful = [t for t in transactions if t.is_success()]
    return {
        "DEPOSIT": sum(t.amount for t in successful if t.type == "DEPOSIT"),
        "WITHDRAW": sum(t.amount for t in successful if t.type == "WITHDRAW"),
    }



def below_minimum(accounts: dict):
    below = list(filter(lambda account: account.is_below_minimum(), accounts.values()))
    return sorted(below, key=lambda account: account.balance)

def counts_and_amounts_by_type(transactions: list):
    report = {}
    for t in transactions:
        if t.type not in report:
            report[t.type] = {"count": 0, "amount": 0.0, "failed": 0}
        if t.is_success():
            report[t.type]["count"] += 1
            report[t.type]["amount"] += t.amount
        else:
            report[t.type]["failed"] += 1
    return dict(sorted(report.items(), key=lambda item: item[1]["amount"], reverse=True))
