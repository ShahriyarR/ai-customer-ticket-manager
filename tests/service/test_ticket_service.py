"""Tests for TicketService"""

from uuid import uuid4

import pytest

from pyticket.domain.tickets.entities import Category, TicketStatus
from pyticket.domain.tickets.exceptions import ClassificationError
from pyticket.service.tickets.dtos import CreateTicketDTO
from pyticket.service.tickets.ticket_service import TicketService


class TestTicketService:
    """Tests for TicketService"""

    def test_create_ticket(self, mock_ai_service, mock_repository):
        """Test creating a ticket."""

        # Make the mock repository return the ticket that was passed to it
        def save_side_effect(ticket):
            return ticket

        mock_repository.save.side_effect = save_side_effect
        service = TicketService(mock_repository, mock_ai_service)

        dto = CreateTicketDTO(title="Test", description="Test description")
        result = service.create_ticket(dto)

        assert result.title == "Test"
        assert result.description == "Test description"
        assert result.category is not None
        assert result.priority is not None
        mock_ai_service.classify_ticket.assert_called_once()
        mock_repository.save.assert_called_once()

    def test_get_ticket(self, mock_repository, classified_ticket):
        """Test getting a ticket."""
        mock_repository.get_by_id.return_value = classified_ticket
        service = TicketService(mock_repository, None)

        result = service.get_ticket(classified_ticket.id)

        assert result is not None
        assert result.id == classified_ticket.id
        assert result.category == Category.TECHNICAL

    def test_get_ticket_not_found(self, mock_repository):
        """Test getting non-existent ticket."""
        mock_repository.get_by_id.return_value = None
        service = TicketService(mock_repository, None)

        result = service.get_ticket(uuid4())

        assert result is None

    def test_list_tickets(self, mock_repository, sample_ticket):
        """Test listing tickets."""
        mock_repository.list_all.return_value = [sample_ticket]
        service = TicketService(mock_repository, None)

        results = service.list_tickets(limit=10, offset=0)

        assert len(results) == 1
        assert results[0].id == sample_ticket.id

    def test_reclassify_ticket(self, mock_ai_service, mock_repository, sample_ticket):
        """Test reclassifying a ticket."""
        mock_repository.get_by_id.return_value = sample_ticket
        mock_repository.update.return_value = sample_ticket
        service = TicketService(mock_repository, mock_ai_service)

        result = service.reclassify_ticket(sample_ticket.id)

        assert result is not None
        mock_ai_service.classify_ticket.assert_called_once()
        mock_repository.update.assert_called_once()

    def test_reclassify_ticket_not_found(self, mock_ai_service, mock_repository):
        """Test reclassifying non-existent ticket."""
        mock_repository.get_by_id.return_value = None
        service = TicketService(mock_repository, mock_ai_service)

        with pytest.raises(ValueError, match="not found"):
            service.reclassify_ticket(uuid4())

    def test_update_ticket_status(self, mock_repository, sample_ticket):
        """Test updating ticket status."""
        mock_repository.get_by_id.return_value = sample_ticket
        mock_repository.update.return_value = sample_ticket
        service = TicketService(mock_repository, None)

        result = service.update_ticket_status(sample_ticket.id, TicketStatus.IN_PROGRESS)

        assert result.status == TicketStatus.IN_PROGRESS
        mock_repository.update.assert_called_once()
