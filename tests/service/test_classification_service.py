"""Tests for TicketClassificationService"""

import pytest

from pyticket.domain.tickets.entities import Category, Priority
from pyticket.domain.tickets.exceptions import ClassificationError
from pyticket.service.tickets.classification_service import TicketClassificationService


class TestTicketClassificationService:
    """Tests for TicketClassificationService"""

    def test_classify_ticket_success(self, mock_ai_service, sample_ticket):
        """Test successful classification."""
        service = TicketClassificationService(mock_ai_service)
        result = service.classify_ticket(sample_ticket)

        assert result.category == Category.TECHNICAL
        assert result.priority == Priority.HIGH
        assert result.confidence_score == 0.95
        mock_ai_service.classify_ticket.assert_called_once_with(sample_ticket)

    def test_classify_ticket_ai_error(self, sample_ticket):
        """Test classification when AI service fails."""
        from unittest.mock import Mock

        mock_ai_service = Mock()
        mock_ai_service.classify_ticket.side_effect = Exception("AI Error")
        service = TicketClassificationService(mock_ai_service)

        with pytest.raises(ClassificationError):
            service.classify_ticket(sample_ticket)
