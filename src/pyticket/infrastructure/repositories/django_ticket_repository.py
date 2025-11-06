"""Django ORM implementation of ticket repository"""

from typing import List, Optional
from uuid import UUID

from pyticket.domain.tickets.entities import Category, Priority, Ticket, TicketStatus
from pyticket.infrastructure.models.models import TicketModel
from pyticket.infrastructure.repositories.interfaces import ITicketRepository


class DjangoTicketRepository(ITicketRepository):
    """Django ORM implementation of ticket repository"""

    def _to_domain(self, model: TicketModel) -> Ticket:
        """Convert Django model to domain entity."""
        ticket = Ticket(
            id=model.id,
            title=model.title,
            description=model.description,
            status=TicketStatus(model.status),
            category=Category(model.category) if model.category else None,
            priority=Priority(model.priority) if model.priority else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return ticket

    def _to_model(self, ticket: Ticket) -> TicketModel:
        """Convert domain entity to Django model."""
        model, _ = TicketModel.objects.get_or_create(id=ticket.id)
        model.title = ticket.title
        model.description = ticket.description
        model.status = ticket.status.value
        model.category = ticket.category.value if ticket.category else None
        model.priority = ticket.priority.value if ticket.priority else None
        model.created_at = ticket.created_at
        model.updated_at = ticket.updated_at
        return model

    def save(self, ticket: Ticket) -> Ticket:
        """Save a ticket."""
        model = self._to_model(ticket)
        model.save()
        return self._to_domain(model)

    def get_by_id(self, ticket_id: UUID) -> Optional[Ticket]:
        """Get a ticket by ID."""
        try:
            model = TicketModel.objects.get(id=ticket_id)
            return self._to_domain(model)
        except TicketModel.DoesNotExist:
            return None

    def list_all(self, limit: int = 100, offset: int = 0) -> List[Ticket]:
        """List all tickets."""
        models = TicketModel.objects.all()[offset : offset + limit]
        return [self._to_domain(model) for model in models]

    def update(self, ticket: Ticket) -> Ticket:
        """Update a ticket."""
        return self.save(ticket)

    def delete(self, ticket_id: UUID) -> bool:
        """Delete a ticket."""
        try:
            TicketModel.objects.get(id=ticket_id).delete()
            return True
        except TicketModel.DoesNotExist:
            return False
