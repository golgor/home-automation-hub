from django.forms import ModelForm

from .models import Cost


class AddCostForm(ModelForm):
    class Meta:
        model = Cost
        fields = ["location", "user", "date", "amount", "excluded_amount", "description"]
