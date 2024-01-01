from typing import Any, TypedDict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View

from .forms import AddCostForm, AddReportForm
from .models import Cost, CostSplitReport


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
        form = AddCostForm()
        context = {
            "form": form,
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

    template_name = "add_report_form.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        """GET method to get the form to add a new cost."""
        unmanaged_costs_items = Cost.objects.filter(included_in_report=None).values(
            "id", "location", "user", "date", "amount", "excluded_amount", "description"
        )
        context = {
            "unmanaged_costs": unmanaged_costs_items,
        }

        return HttpResponse(render(self.request, self.template_name, context))

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """POST method to add a new cost."""
        form = AddReportForm(self.request.POST)
        if form.is_valid():
            assigned_cost_items = form.cleaned_data["cost_list"]
            saved_instance = form.save()
            Cost.objects.filter(id__in=assigned_cost_items).update(included_in_report=saved_instance)

        return redirect("cost_splitter:list_cost")
