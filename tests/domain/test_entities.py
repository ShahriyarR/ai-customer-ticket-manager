"""Tests for domain entities"""

from uuid import uuid4

import pytest

from pyticket.domain.tickets.entities import Category, Priority, Ticket, TicketStatus


class TestTicket:
    """Tests for Ticket entity"""

    def test_create_ticket(self):
        """Test creating a ticket."""
        ticket = Ticket(
            title="Test Ticket",
            description="Test description",
        )
        assert ticket.title == "Test Ticket"
        assert ticket.description == "Test description"
        assert ticket.status == TicketStatus.OPEN
        assert ticket.category is None
        assert ticket.priority is None

    def test_create_ticket_empty_title_raises_error(self):
        """Test that empty title raises error."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            Ticket(title="", description="Test")

    def test_create_ticket_empty_description_raises_error(self):
        """Test that empty description raises error."""
        with pytest.raises(ValueError, match="description cannot be empty"):
            Ticket(title="Test", description="")

    def test_classify_ticket(self, sample_ticket):
        """Test classifying a ticket."""
        sample_ticket.classify(Category.TECHNICAL, Priority.HIGH)
        assert sample_ticket.category == Category.TECHNICAL
        assert sample_ticket.priority == Priority.HIGH
        assert sample_ticket.is_classified()

    def test_is_classified(self, sample_ticket):
        """Test is_classified method."""
        assert not sample_ticket.is_classified()
        sample_ticket.classify(Category.BILLING, Priority.MEDIUM)
        assert sample_ticket.is_classified()

    def test_update_status_valid_transition(self, sample_ticket):
        """Test valid status transition."""
        sample_ticket.update_status(TicketStatus.IN_PROGRESS)
        assert sample_ticket.status == TicketStatus.IN_PROGRESS

    def test_update_status_invalid_transition(self, sample_ticket):
        """Test invalid status transition raises error."""
        sample_ticket.update_status(TicketStatus.IN_PROGRESS)
        with pytest.raises(ValueError):
            sample_ticket.update_status(TicketStatus.CLOSED)


class TestCategory:
    """Tests for Category enum"""

    def test_category_values(self):
        """Test category enum values."""
        assert Category.TECHNICAL.value == "TECHNICAL"
        assert Category.BILLING.value == "BILLING"
        assert Category.FEATURE_REQUEST.value == "FEATURE_REQUEST"
        assert Category.BUG_REPORT.value == "BUG_REPORT"
        assert Category.GENERAL.value == "GENERAL"


class TestPriority:
    """Tests for Priority enum"""

    def test_priority_values(self):
        """Test priority enum values."""
        assert Priority.LOW.value == "LOW"
        assert Priority.MEDIUM.value == "MEDIUM"
        assert Priority.HIGH.value == "HIGH"
        assert Priority.URGENT.value == "URGENT"
