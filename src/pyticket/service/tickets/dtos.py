"""Data Transfer Objects for service layer"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from pyticket.domain.tickets.entities import Category, Priority, TicketStatus


@dataclass
class CreateTicketDTO:
    """DTO for creating a ticket"""

    title: str
    description: str


@dataclass
class ClassificationResultDTO:
    """DTO for classification result"""

    category: Category
    priority: Priority
    confidence_score: float
    reasoning: str


@dataclass
class TicketResponseDTO:
    """DTO for ticket response"""

    id: UUID
    title: str
    description: str
    status: TicketStatus
    category: Optional[Category]
    priority: Optional[Priority]
    created_at: datetime
    updated_at: datetime
    classification: Optional[ClassificationResultDTO] = None
