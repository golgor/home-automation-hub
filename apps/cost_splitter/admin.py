from __future__ import annotations

from django.contrib import admin

from .models import Cost, CostSplitReport, Transaction


class MonthlyReportAdmin(admin.ModelAdmin[CostSplitReport]):
    """Custom admin class for MonthlyReport."""

    resource_class = CostSplitReport
    list_display = ["id", "date", "summed_cost", "description"]

    def summed_cost(self, obj: CostSplitReport):
        """Field to display the summed cost of all costs in a monthly report."""
        return sum(obj.cost_set.select_related("cost_set").values_list("amount", flat=True))


class CostAdmin(admin.ModelAdmin[Cost]):
    """Custom admin class for Cost."""

    resource_class = Cost
    list_display = ["id", "location", "user", "date", "amount", "description", "included_in_report"]


class TransactionAdmin(admin.ModelAdmin[Transaction]):
    """Custom admin class for Cost."""

    resource_class = Transaction
    list_display = ["id", "debtor", "creditor", "amount", "included_in_report", "uuid"]


admin.site.register(Cost, CostAdmin)
admin.site.register(CostSplitReport, MonthlyReportAdmin)
admin.site.register(Transaction, TransactionAdmin)
