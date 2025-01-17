from django.db.models import Sum

from .app_types import Person, Transaction
from .models import Cost


def get_costs_from_report(report_id: int | None) -> dict[Person, float]:
    """Get all costs per person.

    Gets all costs included in a monthly report if report_id is not None, otherwise gets all unmanaged costs.
    Uses annotations to summarize the costs per person and transform the result into a dictionary such as:
    {
        Person(person_id=1, name="Alice"): 10,
        Person(person_id=2, name="Bob"): 20,
    }

    Args:
        report_id (int | None): The id of a CostSplitReport or None.

    Returns:
        dict[Person, float]: A dict with a Person-object as key and the total expenses as value.
    """
    expenses_per_person = (
        Cost.objects.filter(included_in_report=report_id)
        .values("user__id", "user__first_name")
        .annotate(total=Sum("amount"))
    )
    return {
        Person(person_id=entry["user__id"], name=entry["user__first_name"]): entry["total"]
        for entry in expenses_per_person
    }


def calculate_cost_split_for_list_of_costs(expenses: dict[Person, float]) -> list[Transaction]:
    """Performs a cost split for the given list of costs and returns a list of transactions to settle the debts.

    Args:
        expenses (dict[Person, float]): A dict with a Person-object as key and the total expenses as value.

    Returns:
        list[Transaction]: A list of transactions to settle the debts.
    """
    balances = calculate_balances(expenses)
    return minimize_transactions(balances)


def calculate_balances(expenses: dict[Person, float]) -> dict[Person, float]:
    """Calculate net balances for each person based on expenses.

    This creates a dictionary such as:
    {
        Person(person_id=1, name="Alice"): 10,
        Person(person_id=2, name="Bob"): -10,
    }
    Which means that Alice owes Bob 10.
    """
    balances: dict[Person, float] = {
        person: amount - sum(expenses.values()) / len(expenses) for person, amount in expenses.items()
    }
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
