from django.urls import include, path
from rest_framework import routers

from . import api
from .views import AddCostFormView, AddReportFormView, CostsListView, CostSplitReportListView, CostSplitReportView


router = routers.DefaultRouter()
router.register(r"costs", api.CostView, "cost")
router.register(r"reports", api.CostSplitReportView, "report")


urlpatterns = [
    path("<int:id>/", CostSplitReportView.as_view(), name="report"),
    path("", CostSplitReportListView.as_view(), name="list_report"),
    path("costs/", CostsListView.as_view(), name="list_cost"),
    path("add_cost/", AddCostFormView.as_view(), name="add_cost"),
    path("add_report/", AddReportFormView.as_view(), name="add_report"),
    path("api/", include(router.urls)),
]
