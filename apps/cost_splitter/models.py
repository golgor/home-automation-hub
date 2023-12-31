from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class MonthlyReport(models.Model):
    """Model to store monthly reports.

    A monthly report is a collection of costs for a specific month and whether they have been paid or not.
    """

    name = models.CharField(max_length=100)
    date = models.DateField()
    cost_set: models.QuerySet[Cost]

    def __str__(self):
        """String representation of a monthly report."""
        return self.name


class Cost(models.Model):
    """Model for single costs.

    A cost is a single entry of a cost that has been paid by one person.
    """

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    cost = models.FloatField()
    excluded = models.FloatField(default=0.0)
    description = models.TextField()
    monthly_report = models.ForeignKey(MonthlyReport, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        """String representation of a cost line item."""
        return self.name
