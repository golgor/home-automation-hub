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

    cost_list = MultipleChoiceField(required=True)

    class Meta:
        """Meta class for AddReportForm."""

        model = CostSplitReport
        fields = ["date", "description"]
