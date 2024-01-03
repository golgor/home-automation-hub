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

    cost_list = MultipleChoiceField(
        required=True, choices=Cost.objects.filter(included_in_report=None).values_list("id", "location")
    )

    class Meta:
        """Meta class for AddReportForm."""

        model = CostSplitReport
        fields = ["date", "description"]
