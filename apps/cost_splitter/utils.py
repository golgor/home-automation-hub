from django.db.models import Sum

from .models import Cost, CostSplitReport
from .types import Person, Transaction


def calculate_cost_split(report: CostSplitReport) -> list[Transaction]:
    """Calculate the cost split for a monthly report."""
    expenses = get_total_expenses(report)
    balances = calculate_balances(expenses)
    return minimize_transactions(balances)


def get_total_expenses(report: CostSplitReport) -> dict[Person, float]:
    """Get total expenses for each person."""
    expenses_per_person = (
        Cost.objects.filter(included_in_report=report)
        .values("user__id", "user__first_name")
        .annotate(total=Sum("amount"))
    )
    return {
        Person(person_id=entry["user__id"], name=entry["user__first_name"]): entry["total"]
        for entry in expenses_per_person
    }


def calculate_balances(expenses: dict[Person, float]) -> dict[Person, float]:
    """Calculate net balances for each person based on expenses.

    This creates a dictionary such as:
    {
        Person(person_id=1, name="Alice"): 10,
        Person(person_id=2, name="Bob"): -10,
    }
    Which means that Alice owes Bob 10.
    """
    balances: dict[Person, float] = {}
    for person, amount in expenses.items():
        # Deduct the average expense from each person's expense
        balances[person] = amount - sum(expenses.values()) / len(expenses)
    return balances


def minimize_transactions(balances: dict[Person, float]):
    """Arrange transactions to settle debts with minimum number of transactions.

    Notice that there are two limits for the transaction:

    1. If the debtor have enough balance, the transaction amount is the total debt of the creditor. The creditor is
        then popped from the list as he/she doesn't have any more credits to gain.
    2. If the debtor does not have enough balance, the transaction amount is the creditors outstanding balance.
        The debtor is then popped from the list as he/she does not have any more debts to settle.
    3. If the debtor and creditor have the same balance, both are popped from the list as they are settled.
    """
    # Create two lists: one for debtors (negative balance) and one for creditors (positive balance)
    debtors = [(person, -balance) for person, balance in balances.items() if balance < 0]
    creditors = [(person, balance) for person, balance in balances.items() if balance > 0]

    transactions: list[Transaction] = []

    # Process as long as there are debtors and creditors
    while debtors and creditors:
        debtor, debt_amount = debtors[0]
        creditor, credit_amount = creditors[0]

        # Determine the transaction amount
        transaction_amount = min(debt_amount, credit_amount)
        transactions.append(Transaction(debtor, creditor, transaction_amount))

        # Update the amounts, remove the person from the list if their balance is settled
        if debt_amount > credit_amount:
            debtors[0] = (debtor, debt_amount - credit_amount)
            creditors.pop(0)
        elif debt_amount < credit_amount:
            creditors[0] = (creditor, credit_amount - debt_amount)
            debtors.pop(0)
        else:  # debt_amount == credit_amount
            debtors.pop(0)
            creditors.pop(0)

    return transactions
