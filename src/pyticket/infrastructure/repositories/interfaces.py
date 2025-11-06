"""Repository interfaces"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from pyticket.domain.tickets.entities import Ticket


class ITicketRepository(ABC):
    """Interface for ticket repository"""

    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        """Save a ticket."""

    @abstractmethod
    def get_by_id(self, ticket_id: UUID) -> Optional[Ticket]:
        """Get a ticket by ID."""

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[Ticket]:
        """List all tickets."""

    @abstractmethod
    def update(self, ticket: Ticket) -> Ticket:
        """Update a ticket."""

    @abstractmethod
    def delete(self, ticket_id: UUID) -> bool:
        """Delete a ticket."""
