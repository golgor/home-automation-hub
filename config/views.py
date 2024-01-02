from typing import Any

from django.views.generic.base import TemplateView


class MainApplicationView(TemplateView):
    """View to display a list of all CostSplitReports."""

    template_name = "main.html"

    def get_context_data(self, **kwargs: Any):
        """Adds 'reports' to the context.

        Intention is to have a list of apps with entry points, even if the url works, it doesn't work in a
        loop with variables for some reason.
        """
        context = super().get_context_data(**kwargs)
        context["registrered_apps"] = {"cost_splitter": "list_report"}
        return context
