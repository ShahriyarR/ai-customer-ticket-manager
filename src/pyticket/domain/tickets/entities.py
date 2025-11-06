"""Domain entities for tickets"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class Category(Enum):
    """Ticket category enumeration"""

    TECHNICAL = "TECHNICAL"
    BILLING = "BILLING"
    FEATURE_REQUEST = "FEATURE_REQUEST"
    BUG_REPORT = "BUG_REPORT"
    GENERAL = "GENERAL"


class Priority(Enum):
    """Ticket priority enumeration"""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class TicketStatus(Enum):
    """Ticket status enumeration"""

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


@dataclass
class Ticket:
    """Ticket domain entity"""

    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    status: TicketStatus = TicketStatus.OPEN
    category: Optional[Category] = None
    priority: Optional[Priority] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate ticket after initialization."""
        if not self.title:
            raise ValueError("Ticket title cannot be empty")
        if not self.description:
            raise ValueError("Ticket description cannot be empty")

    def update_status(self, new_status: TicketStatus) -> None:
        """Update ticket status with validation."""
        valid_transitions = {
            TicketStatus.OPEN: [TicketStatus.IN_PROGRESS, TicketStatus.CLOSED],
            TicketStatus.IN_PROGRESS: [TicketStatus.RESOLVED, TicketStatus.OPEN],
            TicketStatus.RESOLVED: [TicketStatus.CLOSED, TicketStatus.IN_PROGRESS],
            TicketStatus.CLOSED: [],
        }

        if new_status not in valid_transitions.get(self.status, []):
            raise ValueError(f"Cannot transition from {self.status.value} to {new_status.value}")

        self.status = new_status
        self.updated_at = datetime.utcnow()

    def classify(self, category: Category, priority: Priority) -> None:
        """Classify ticket with category and priority."""
        self.category = category
        self.priority = priority
        self.updated_at = datetime.utcnow()

    def is_classified(self) -> bool:
        """Check if ticket is classified."""
        return self.category is not None and self.priority is not None
