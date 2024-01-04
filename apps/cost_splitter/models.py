from __future__ import annotations

import uuid

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class CostSplitReport(models.Model):
    """Model to store monthly reports.

    A monthly report is a collection of costs for a specific month and whether they have been paid or not.
    """

    date = models.DateField()
    cost_set: models.QuerySet[Cost]
    transactions: models.QuerySet[Transaction]
    description = models.TextField(blank=True, default="")

    def __str__(self):
        """String representation of a monthly report."""
        return str(self.date)


class Cost(models.Model):
    """Model for single costs.

    A cost is a single entry of a cost that has been paid by one person.
    """

    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    amount = models.FloatField()
    description = models.TextField(blank=True, default="")
    included_in_report = models.ForeignKey(
        CostSplitReport, on_delete=models.SET_NULL, blank=True, default=None, null=True
    )

    def __str__(self):
        """String representation of a cost line item."""
        return self.location


class Transaction(models.Model):
    """Model for a transaction.

    Debtor is the person who owes money and is paying to the creditor.
    """

    debtor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="debit_transactions")
    creditor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="credit_transactions")
    amount = models.FloatField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    included_in_report = models.ForeignKey(
        CostSplitReport, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name="transactions"
    )

    def __str__(self):
        """String representation of a transaction."""
        return f"{self.debtor} -> {self.creditor}: {self.amount}"
