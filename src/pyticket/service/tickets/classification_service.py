"""Ticket classification service"""

import logging

from pyticket.domain.tickets.entities import Ticket
from pyticket.domain.tickets.exceptions import ClassificationError
from pyticket.domain.tickets.services import TicketClassificationService as DomainClassificationService
from pyticket.infrastructure.ai.interfaces import AIClassificationService, ClassificationResult

logger = logging.getLogger(__name__)


class TicketClassificationService:
    """Service for orchestrating ticket classification"""

    def __init__(self, ai_service: AIClassificationService):
        """
        Initialize classification service.

        Args:
            ai_service: AI classification service implementation
        """
        self.ai_service = ai_service
        self.domain_service = DomainClassificationService()

    def classify_ticket(self, ticket: Ticket) -> ClassificationResult:
        """
        Classify a ticket using AI and apply business rules.

        Args:
            ticket: The ticket to classify

        Returns:
            ClassificationResult with category, priority, confidence, and reasoning

        Raises:
            ClassificationError: If classification fails
        """
        try:
            # Use AI service to classify
            result = self.ai_service.classify_ticket(ticket)

            # Apply domain validation rules
            if not self.domain_service.validate_classification(result.category, result.priority):
                logger.warning(
                    f"Invalid classification combination: {result.category.value}, " f"{result.priority.value}. Adjusting priority."
                )
                # Adjust priority if invalid combination
                result.priority = self.domain_service.get_default_priority_for_category(result.category)

            logger.info(
                f"Successfully classified ticket {ticket.id}: "
                f"{result.category.value}, {result.priority.value}, "
                f"confidence: {result.confidence_score}"
            )

            return result
        except Exception as e:
            logger.error(f"Classification failed for ticket {ticket.id}: {e}")
            raise ClassificationError(f"Failed to classify ticket: {str(e)}") from e
