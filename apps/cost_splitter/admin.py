from __future__ import annotations

from django.contrib import admin

from .models import Cost, MonthlyReport


class MonthlyReportAdmin(admin.ModelAdmin[MonthlyReport]):
    """Custom admin class for MonthlyReport."""

    resource_class = MonthlyReport
    list_display = ["id", "name", "date", "summed_cost"]

    def summed_cost(self, obj: MonthlyReport):
        """Field to display the summed cost of all costs in a monthly report."""
        return sum(obj.cost_set.select_related("cost_set").values_list("cost", flat=True))


class CostAdmin(admin.ModelAdmin[Cost]):
    """Custom admin class for Cost."""

    resource_class = Cost
    list_display = ["id", "name", "user", "date", "cost", "excluded", "description", "monthly_report"]


admin.site.register(Cost, CostAdmin)
admin.site.register(MonthlyReport, MonthlyReportAdmin)
