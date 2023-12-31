from typing import TypedDict

from django.views.generic.base import TemplateView

from .models import Cost, MonthlyReport


class MonthlyReportContext(TypedDict):
    """Type definition for the extra context passed to the view."""

    year: int
    month: int


# Create your views here.
class MonthlyReportView(TemplateView):
    """View to display a monthly report."""

    template_name = "home.html"

    def get_context_data(self, **kwargs: MonthlyReportContext):
        """View to display a monthly report."""
        context = super().get_context_data(**kwargs)

        try:
            monthly_report = MonthlyReport.objects.get(date__year=context["year"], date__month=context["month"])
        except MonthlyReport.DoesNotExist:
            return {"error": "Monthly report does not exist."}

        costs = Cost.objects.filter(monthly_report=monthly_report)

        context["costs"] = costs
        return context
