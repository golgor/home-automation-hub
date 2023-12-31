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
        year = kwargs["year"]
        month = kwargs["month"]

        try:
            monthly_report = MonthlyReport.objects.get(date__year=year, date__month=month)
        except MonthlyReport.DoesNotExist:
            monthly_report = None

        if monthly_report is None:
            return {"error": "Monthly report does not exist."}
        costs = Cost.objects.filter(monthly_report=monthly_report)
        context = {
            "year": year,
            "month": month,
            "costs": costs,
        }
        context2 = super().get_context_data(**kwargs)
        print(f"Context2: {context2}")
        return context
