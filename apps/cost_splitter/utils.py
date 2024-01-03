from typing import TypedDict

from django.db.models import Sum

from .models import Cost, CostSplitReport


class Transaction(TypedDict):
    """Type definition for a transaction."""

    from_: str
    to: str
    amount: int


def calculate_cost_split(report: CostSplitReport) -> list[Transaction]:
    """Calculate the cost split for a monthly report."""
    costs_per_user = (
        Cost.objects.filter(included_in_report=report)
        .values("user__id", "user__first_name")
        .annotate(total=Sum("amount"))
    )
    total_cost = Cost.objects.filter(included_in_report=report).aggregate(Sum("amount"))
    for user in costs_per_user:
        user["diff"] = user["total"] - (total_cost["amount__sum"] / len(costs_per_user))
    outstanding_differences = sorted(costs_per_user, key=lambda k: k["diff"], reverse=True)

    transactions: list[Transaction] = []

    while outstanding_differences:
        highest_diff = outstanding_differences[0]
        lowest_diff = outstanding_differences[-1]
        transactions.append(
            {
                "to": highest_diff["user__first_name"],
                "from_": lowest_diff["user__first_name"],
                "amount": highest_diff["diff"],
            }
        )
        highest_diff["diff"] += lowest_diff["diff"]
        lowest_diff["diff"] = 0
        if highest_diff["diff"] >= 0:
            outstanding_differences.pop()
        if lowest_diff["diff"] <= 0:
            outstanding_differences.pop()
    return transactions
