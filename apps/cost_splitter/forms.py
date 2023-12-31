from django.forms import ModelForm

from .models import Cost


class AddCostForm(ModelForm):
    """Form used to add a new cost."""

    class Meta:
        """Meta class for AddCostForm."""

        model = Cost
        fields = ["location", "user", "date", "amount", "excluded_amount", "description"]
