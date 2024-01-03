from typing import Any, TypedDict

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View

from .forms import AddCostForm, AddReportForm
from .models import Cost, CostSplitReport, Transaction
from .utils import calculate_cost_split


User = get_user_model()


class MonthlyReportContext(TypedDict):
    """Type definition for the extra context passed to the view."""

    id: int


# Create your views here.
class CostSplitReportView(TemplateView):
    """View to display a CostSplitReport."""

    template_name = "report_id.html"

    def get_context_data(self, **kwargs: MonthlyReportContext):
        """Adds 'costs' to the context."""
        context = super().get_context_data(**kwargs)

        try:
            report = CostSplitReport.objects.get(id=context["id"])
        except CostSplitReport.DoesNotExist:
            return {"error": "Monthly report does not exist."}

        costs = Cost.objects.filter(included_in_report=report)
        context["costs"] = costs
        context["report"] = report
        return context


class CostsListView(TemplateView):
    """View to display a list of all costs.

    Returns both costs that are included in a monthly report and those that are not.
    """

    template_name = "costs_list.html"

    def get_context_data(self, **kwargs: Any):
        """Add 'unmanaged_costs' and 'managed_costs' to the context."""
        context = super().get_context_data(**kwargs)

        unmanaged_costs = Cost.objects.filter(included_in_report=None)
        managed_costs = Cost.objects.exclude(included_in_report=None)

        context["unmanaged_costs"] = unmanaged_costs
        context["managed_costs"] = managed_costs
        return context


class CostSplitReportListView(TemplateView):
    """View to display a list of all CostSplitReports."""

    template_name = "report_list.html"

    def get_context_data(self, **kwargs: Any):
        """Adds 'reports' to the context."""
        context = super().get_context_data(**kwargs)

        try:
            reports = CostSplitReport.objects.all()
        except CostSplitReport.DoesNotExist:
            return {"error": "No reports found!"}

        context["reports"] = reports

        return context


class AddCostFormView(View):
    """View to add a new cost using a form."""

    template_name = "add_cost_form.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        """GET method to get the form to add a new cost."""
        users = User.objects.all()
        context = {
            "users": users,
        }

        return HttpResponse(render(self.request, self.template_name, context))

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """POST method to add a new cost."""
        form = AddCostForm(self.request.POST)
        if form.is_valid():
            form.save()

        return redirect("cost_splitter:list_cost")


class AddReportFormView(View):
    """View to add a new report using a form."""

    template_name = "add_cost_split_form.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        """GET method to get the form to add a new cost."""
        context = {
            "unmanaged_costs": self.get_unmanaged_costs(),
        }

        return HttpResponse(render(self.request, self.template_name, context))

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """POST method to add a new cost."""
        form = AddReportForm(self.request.POST)
        if form.is_valid():
            assigned_cost_items = form.cleaned_data["cost_list"]
            report: CostSplitReport = form.save()
            Cost.objects.filter(id__in=assigned_cost_items).update(included_in_report=report)
            transactions = calculate_cost_split(report)
            for transaction in transactions:
                Transaction.objects.create(
                    debtor=User.objects.get(id=transaction.debtor.person_id),
                    creditor=User.objects.get(id=transaction.creditor.person_id),
                    amount=transaction.amount,
                    included_in_report=report,
                )
            return redirect("cost_splitter:report", id=report.pk)

        context = {
            "form": form,
            "unmanaged_costs": self.get_unmanaged_costs(),
        }
        return HttpResponse(render(self.request, self.template_name, context))

    @staticmethod
    def get_unmanaged_costs():
        """Get all costs that are not assigned to a monthly report."""
        return Cost.objects.filter(included_in_report=None).values(
            "id", "location", "user__id", "user__first_name", "date", "amount", "description"
        )
