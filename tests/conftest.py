"""Pytest configuration and fixtures"""

import os

import django
from django.conf import settings

# Configure Django settings for pytest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyticket.configurator.settings")
django.setup()

from unittest.mock import Mock
from uuid import uuid4

import pytest

from pyticket.domain.tickets.entities import Category, Priority, Ticket, TicketStatus
from pyticket.infrastructure.ai.interfaces import AIClassificationService, ClassificationResult
from pyticket.infrastructure.repositories.interfaces import ITicketRepository


@pytest.fixture
def sample_ticket():
    """Create a sample ticket for testing."""
    return Ticket(
        id=uuid4(),
        title="Test Ticket",
        description="This is a test ticket description",
        status=TicketStatus.OPEN,
    )


@pytest.fixture
def classified_ticket():
    """Create a classified ticket for testing."""
    ticket = Ticket(
        id=uuid4(),
        title="Technical Issue",
        description="I'm having trouble logging in",
        status=TicketStatus.OPEN,
    )
    ticket.classify(Category.TECHNICAL, Priority.HIGH)
    return ticket


@pytest.fixture
def mock_ai_service():
    """Create a mock AI classification service."""
    service = Mock(spec=AIClassificationService)
    service.classify_ticket.return_value = ClassificationResult(
        category=Category.TECHNICAL,
        priority=Priority.HIGH,
        confidence_score=0.95,
        reasoning="Technical login issue",
    )
    return service


@pytest.fixture
def mock_repository():
    """Create a mock ticket repository."""
    repository = Mock(spec=ITicketRepository)
    return repository
