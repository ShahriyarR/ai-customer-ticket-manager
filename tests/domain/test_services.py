"""Tests for domain services"""

import pytest

from pyticket.domain.tickets.entities import Category, Priority
from pyticket.domain.tickets.services import TicketClassificationService, TicketRoutingService


class TestTicketClassificationService:
    """Tests for TicketClassificationService"""

    def test_validate_classification_valid(self):
        """Test valid classification combination."""
        assert TicketClassificationService.validate_classification(Category.TECHNICAL, Priority.HIGH)

    def test_validate_classification_invalid(self):
        """Test invalid classification combination."""
        assert not TicketClassificationService.validate_classification(Category.GENERAL, Priority.URGENT)

    def test_get_default_priority_for_category(self):
        """Test getting default priority for category."""
        assert TicketClassificationService.get_default_priority_for_category(Category.TECHNICAL) == Priority.MEDIUM
        assert TicketClassificationService.get_default_priority_for_category(Category.BILLING) == Priority.HIGH
        assert TicketClassificationService.get_default_priority_for_category(Category.FEATURE_REQUEST) == Priority.LOW


class TestTicketRoutingService:
    """Tests for TicketRoutingService"""

    def test_get_team_for_category(self):
        """Test getting team for category."""
        assert TicketRoutingService.get_team_for_category(Category.TECHNICAL) == "technical-support"
        assert TicketRoutingService.get_team_for_category(Category.BILLING) == "billing-team"
        assert TicketRoutingService.get_team_for_category(Category.FEATURE_REQUEST) == "product-team"
        assert TicketRoutingService.get_team_for_category(Category.BUG_REPORT) == "engineering-team"
        assert TicketRoutingService.get_team_for_category(Category.GENERAL) == "customer-support"
