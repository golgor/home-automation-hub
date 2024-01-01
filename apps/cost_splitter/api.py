from rest_framework import viewsets

from .models import Cost, CostSplitReport
from .serializers import CostSerializer, CostSplitReportSerializer


class CostView(viewsets.ModelViewSet):
    """ModelViewSet for the Cost Model."""

    serializer_class = CostSerializer
    queryset = Cost.objects.all()


class CostSplitReportView(viewsets.ModelViewSet):
    """ModelViewSet for the CostSplitReport Model."""

    serializer_class = CostSplitReportSerializer
    queryset = CostSplitReport.objects.all()
