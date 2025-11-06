"""Tests for repository implementations"""

from uuid import uuid4

import pytest

from pyticket.domain.tickets.entities import Category, Priority, Ticket, TicketStatus
from pyticket.infrastructure.repositories.django_ticket_repository import DjangoTicketRepository


@pytest.mark.django_db
class TestDjangoTicketRepository:
    """Tests for DjangoTicketRepository"""

    def test_save_ticket(self):
        """Test saving a ticket."""
        ticket = Ticket(
            title="Test Ticket",
            description="Test description",
        )
        repository = DjangoTicketRepository()
        saved = repository.save(ticket)

        assert saved.id == ticket.id
        assert saved.title == "Test Ticket"

    def test_get_by_id(self):
        """Test getting ticket by ID."""
        ticket = Ticket(
            title="Test Ticket",
            description="Test description",
        )
        repository = DjangoTicketRepository()
        saved = repository.save(ticket)

        retrieved = repository.get_by_id(saved.id)
        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.title == "Test Ticket"

    def test_get_by_id_not_found(self):
        """Test getting non-existent ticket."""
        repository = DjangoTicketRepository()
        result = repository.get_by_id(uuid4())
        assert result is None

    def test_list_all(self):
        """Test listing all tickets."""
        repository = DjangoTicketRepository()
        ticket1 = repository.save(Ticket(title="Ticket 1", description="Description 1"))
        ticket2 = repository.save(Ticket(title="Ticket 2", description="Description 2"))

        tickets = repository.list_all(limit=10, offset=0)
        assert len(tickets) >= 2
        ids = [t.id for t in tickets]
        assert ticket1.id in ids
        assert ticket2.id in ids

    def test_update_ticket(self):
        """Test updating a ticket."""
        ticket = Ticket(
            title="Original Title",
            description="Original description",
        )
        repository = DjangoTicketRepository()
        saved = repository.save(ticket)

        saved.title = "Updated Title"
        updated = repository.update(saved)

        assert updated.title == "Updated Title"
        retrieved = repository.get_by_id(saved.id)
        assert retrieved.title == "Updated Title"

    def test_delete_ticket(self):
        """Test deleting a ticket."""
        ticket = Ticket(
            title="Test Ticket",
            description="Test description",
        )
        repository = DjangoTicketRepository()
        saved = repository.save(ticket)

        result = repository.delete(saved.id)
        assert result is True

        retrieved = repository.get_by_id(saved.id)
        assert retrieved is None
