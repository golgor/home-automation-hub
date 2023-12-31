from typing import TypedDict

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView, View

from .forms import AddCostForm
from .models import Cost, CostSplitReport


class MonthlyReportContext(TypedDict):
    """Type definition for the extra context passed to the view."""

    id: int


# Create your views here.
class CostSplitReportView(TemplateView):
    """View to display a monthly report."""

    template_name = "report_id.html"

    def get_context_data(self, **kwargs: MonthlyReportContext):
        """View to display a monthly report."""
        context = super().get_context_data(**kwargs)

        try:
            report = CostSplitReport.objects.get(id=context["id"])
        except CostSplitReport.DoesNotExist:
            return {"error": "Monthly report does not exist."}

        costs = Cost.objects.filter(included_in_report=report)

        context["costs"] = costs
        return context


class CostsListView(TemplateView):
    """View to display a monthly report."""

    template_name = "costs_list.html"

    def get_context_data(self, **kwargs):
        """View to display a monthly report."""
        context = super().get_context_data(**kwargs)

        unmanaged_costs = Cost.objects.filter(included_in_report=None)
        managed_costs = Cost.objects.exclude(included_in_report=None)

        context["unmanaged_costs"] = unmanaged_costs
        context["managed_costs"] = managed_costs
        return context


class CostSplitReportListView(TemplateView):
    """View to display a monthly report."""

    template_name = "report_list.html"

    def get_context_data(self, **kwargs):
        """View to display a monthly report."""
        context = super().get_context_data(**kwargs)

        try:
            report = CostSplitReport.objects.all()
        except CostSplitReport.DoesNotExist:
            return {"error": "Monthly report does not exist."}

        context["reports"] = report

        return context


class AddCostFormView(View):
    """View to display a monthly report."""

    template_name = "add_cost_form.html"

    def get(self, request, *args, **kwargs):
        """View to display a monthly report."""

        form = AddCostForm()
        context = {
            "form": form,
        }

        return HttpResponse(render(self.request, self.template_name, context))

    def post(self, request, *args, **kwargs):
        """View to display a monthly report."""

        form = AddCostForm(self.request.POST)
        if form.is_valid():
            form.save()

        return redirect("cost_splitter:list_cost")
