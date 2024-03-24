from datetime import datetime
from zoneinfo import ZoneInfo

from apps.cost_splitter.models import CostSplitReport


class TestCostSplitReport:
    """Test class for the CostSplitReport model."""

    def test_string_representation(self) -> None:
        """Test the string representation of a cost line item."""
        report = CostSplitReport(date=datetime(2024, 4, 1, 12, 0, 0, tzinfo=ZoneInfo("UTC")))
        assert str(report) == "2024-04-01 12:00:00+00:00"


class TestCost:
    """Test class for the Cost model."""

    def test_string_representation(self) -> None:
        """Test the string representation of a cost line item.

        Not implemented, this needs Users which likely should be implemented using fixtures.
        """
        assert True


class TestTransaction:
    """Test class for the Transaction model."""

    def test_string_representation(self) -> None:
        """Test the string representation of a transaction.

        Not implemented, this needs Users which likely should be implemented using fixtures.
        """
        assert True
