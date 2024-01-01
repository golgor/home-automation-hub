from rest_framework import serializers

from .models import Cost, CostSplitReport


class CostSerializer(serializers.ModelSerializer[Cost]):
    """Serializer for the Cost Model.

    This is used in api.CostView().
    """

    class Meta:
        """Meta class for the CostSerializer."""

        model = Cost
        fields = "__all__"


class CostSplitReportSerializer(serializers.ModelSerializer[CostSplitReport]):
    """Serializer for the CostSplitReport Model.

    This is used in api.CostSplitReportView().
    """

    class Meta:
        """Meta class for the CostSplitReportSerializer."""

        model = CostSplitReport
        fields = "__all__"
