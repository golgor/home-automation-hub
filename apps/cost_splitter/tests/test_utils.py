from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model

from apps.cost_splitter.models import CostSplitReport
from apps.cost_splitter.types import Person
from apps.cost_splitter.utils import get_total_expenses


User = get_user_model()


@pytest.mark.django_db
def test_get_total_expenses():
    """Test the get_total_expenses function.

    This is testing only the dict comprehension part of the function. The rest is a query using django ORM.
    """
    report = CostSplitReport.objects.create(date="2021-01-01")

    # Create some mock Cost objects
    cost1 = {"user__id": 1, "user__first_name": "John", "total": 10}
    cost2 = {"user__id": 2, "user__first_name": "Jane", "total": 20}
    cost3 = {"user__id": 3, "user__first_name": "Bob", "total": 15}

    # Mock the Cost.objects.filter method to return a MagicMock
    with patch("apps.cost_splitter.utils.Cost.objects.filter") as mock_filter:
        # Create a MagicMock for ORM operations
        mock_filter.return_value.values.return_value.annotate.return_value = [cost1, cost2, cost3]

        result = get_total_expenses(report)

        assert result == {
            Person(person_id=1, name="John"): 10.0,
            Person(person_id=2, name="Jane"): 20.0,
            Person(person_id=3, name="Bob"): 15.0,
        }
