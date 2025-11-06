"""Dependency injection for API endpoints"""

from pyticket.infrastructure.ai.factory import AIClassificationServiceFactory
from pyticket.infrastructure.repositories.django_ticket_repository import DjangoTicketRepository
from pyticket.service.tickets.ticket_service import TicketService


def get_ticket_service() -> TicketService:
    """Get ticket service instance with dependencies injected."""
    repository = DjangoTicketRepository()
    ai_service = AIClassificationServiceFactory.create()
    return TicketService(repository=repository, ai_classification_service=ai_service)
