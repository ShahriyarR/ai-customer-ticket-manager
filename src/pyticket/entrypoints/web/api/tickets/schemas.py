"""Request/Response schemas for tickets API"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema


class TicketCreateSchema(Schema):
    """Schema for creating a ticket"""

    title: str
    description: str


class ClassificationResultSchema(Schema):
    """Schema for classification result"""

    category: str
    priority: str
    confidence_score: float
    reasoning: str


class TicketResponseSchema(Schema):
    """Schema for ticket response"""

    id: UUID
    title: str
    description: str
    status: str
    category: Optional[str] = None
    priority: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    classification: Optional[ClassificationResultSchema] = None


class TicketUpdateStatusSchema(Schema):
    """Schema for updating ticket status"""

    status: str
