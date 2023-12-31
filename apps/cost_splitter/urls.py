from django.urls import path

from .views import CostsListView, CostSplitReportListView, CostSplitReportView


urlpatterns = [
    path("<int:id>/", CostSplitReportView.as_view(), name="monthly_report_view"),
    path("", CostSplitReportListView.as_view(), name="monthly_report_view"),
    path("costs/", CostsListView.as_view(), name="monthly_report_view"),
]
