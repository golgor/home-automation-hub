from typing import Any

from django.forms import CheckboxSelectMultiple, ModelForm, MultipleChoiceField

from .models import Cost, CostSplitReport


class AddCostForm(ModelForm):
    """Form used to add a new cost."""

    class Meta:
        """Meta class for AddCostForm."""

        model = Cost
        fields = ["location", "user", "date", "amount", "description"]


class AddReportForm(ModelForm):
    """Form used to add a new report."""

    cost_list = MultipleChoiceField(required=False, widget=CheckboxSelectMultiple)

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize the form to enable dynamic choices for the cost_list field."""
        super().__init__(*args, **kwargs)
        unmanaged_costs_items = Cost.objects.filter(included_in_report=None).values("id", "location", "description")
        unmanaged_costs = [
            (cost_item["id"], f"{cost_item["location"]} - {cost_item["description"]}")
            for cost_item in unmanaged_costs_items
        ]
        self.fields["cost_list"].choices = unmanaged_costs

    class Meta:
        """Meta class for AddReportForm."""

        model = CostSplitReport
        fields = ["date", "description"]
