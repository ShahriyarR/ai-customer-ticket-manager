"""Ticket management service"""

import logging
from typing import List, Optional
from uuid import UUID

from pyticket.domain.tickets.entities import Ticket, TicketStatus
from pyticket.domain.tickets.exceptions import InvalidTicketStatusError
from pyticket.domain.tickets.services import TicketRoutingService
from pyticket.infrastructure.ai.interfaces import AIClassificationService
from pyticket.infrastructure.repositories.interfaces import ITicketRepository
from pyticket.service.tickets.classification_service import TicketClassificationService
from pyticket.service.tickets.dtos import ClassificationResultDTO, CreateTicketDTO, TicketResponseDTO

logger = logging.getLogger(__name__)


class TicketService:
    """Service for managing tickets"""

    def __init__(
        self,
        repository: ITicketRepository,
        ai_classification_service: AIClassificationService,
    ):
        """
        Initialize ticket service.

        Args:
            repository: Ticket repository
            ai_classification_service: AI classification service
        """
        self.repository = repository
        self.classification_service = TicketClassificationService(ai_classification_service)
        self.routing_service = TicketRoutingService()

    def create_ticket(self, dto: CreateTicketDTO) -> TicketResponseDTO:
        """
        Create a new ticket and classify it.

        Args:
            dto: Ticket creation data

        Returns:
            TicketResponseDTO with ticket and classification information
        """
        # Create domain entity
        ticket = Ticket(title=dto.title, description=dto.description)

        # Classify ticket
        classification_result = self.classification_service.classify_ticket(ticket)

        # Apply classification to ticket
        ticket.classify(classification_result.category, classification_result.priority)

        # Get routing information
        team = self.routing_service.get_team_for_category(classification_result.category)
        logger.info(f"Ticket {ticket.id} routed to team: {team}")

        # Save ticket
        saved_ticket = self.repository.save(ticket)

        # Convert to DTO
        return self._to_response_dto(saved_ticket, classification_result)

    def get_ticket(self, ticket_id: UUID) -> Optional[TicketResponseDTO]:
        """
        Get a ticket by ID.

        Args:
            ticket_id: Ticket ID

        Returns:
            TicketResponseDTO or None if not found
        """
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            return None

        classification = None
        if ticket.is_classified():
            classification = ClassificationResultDTO(
                category=ticket.category,
                priority=ticket.priority,
                confidence_score=0.0,  # Not stored, would need to be retrieved separately
                reasoning="",
            )

        return self._to_response_dto(ticket, classification)

    def list_tickets(self, limit: int = 100, offset: int = 0) -> List[TicketResponseDTO]:
        """
        List tickets.

        Args:
            limit: Maximum number of tickets to return
            offset: Number of tickets to skip

        Returns:
            List of TicketResponseDTO
        """
        tickets = self.repository.list_all(limit=limit, offset=offset)
        return [self._to_response_dto(ticket, None) for ticket in tickets]

    def reclassify_ticket(self, ticket_id: UUID) -> TicketResponseDTO:
        """
        Reclassify a ticket.

        Args:
            ticket_id: Ticket ID

        Returns:
            TicketResponseDTO with updated classification

        Raises:
            ValueError: If ticket not found
        """
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket {ticket_id} not found")

        # Classify ticket
        classification_result = self.classification_service.classify_ticket(ticket)

        # Apply classification to ticket
        ticket.classify(classification_result.category, classification_result.priority)

        # Update ticket
        updated_ticket = self.repository.update(ticket)

        logger.info(f"Reclassified ticket {ticket_id}")

        return self._to_response_dto(updated_ticket, classification_result)

    def update_ticket_status(self, ticket_id: UUID, new_status: TicketStatus) -> TicketResponseDTO:
        """
        Update ticket status.

        Args:
            ticket_id: Ticket ID
            new_status: New status

        Returns:
            TicketResponseDTO with updated status

        Raises:
            ValueError: If ticket not found
            InvalidTicketStatusError: If status transition is invalid
        """
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket {ticket_id} not found")

        try:
            ticket.update_status(new_status)
        except ValueError as e:
            raise InvalidTicketStatusError(str(e)) from e

        updated_ticket = self.repository.update(ticket)

        return self._to_response_dto(updated_ticket, None)

    def _to_response_dto(
        self,
        ticket: Ticket,
        classification: Optional[ClassificationResultDTO],
    ) -> TicketResponseDTO:
        """Convert domain entity to response DTO."""
        classification_dto = classification
        if not classification_dto and ticket.is_classified():
            classification_dto = ClassificationResultDTO(
                category=ticket.category,
                priority=ticket.priority,
                confidence_score=0.0,
                reasoning="",
            )

        return TicketResponseDTO(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            status=ticket.status,
            category=ticket.category,
            priority=ticket.priority,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            classification=classification_dto,
        )
