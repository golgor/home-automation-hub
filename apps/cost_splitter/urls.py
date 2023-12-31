from django.urls import path

from .views import AddCostFormView, CostsListView, CostSplitReportListView, CostSplitReportView


urlpatterns = [
    path("<int:id>/", CostSplitReportView.as_view(), name="report"),
    path("", CostSplitReportListView.as_view(), name="list_report"),
    path("costs/", CostsListView.as_view(), name="list_cost"),
    path("costs/add/", AddCostFormView.as_view(), name="add_cost"),
]
