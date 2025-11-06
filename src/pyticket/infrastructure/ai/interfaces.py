"""Abstract AI service interface"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from pyticket.domain.tickets.entities import Category, Priority, Ticket


@dataclass
class ClassificationResult:
    """Result of AI classification"""

    category: Category
    priority: Priority
    confidence_score: float
    reasoning: str


class AIClassificationService(ABC):
    """Abstract interface for AI classification service"""

    @abstractmethod
    def classify_ticket(self, ticket: Ticket) -> ClassificationResult:
        """
        Classify a ticket using AI.

        Args:
            ticket: The ticket to classify

        Returns:
            ClassificationResult with category, priority, confidence, and reasoning

        Raises:
            ClassificationError: If classification fails
        """
