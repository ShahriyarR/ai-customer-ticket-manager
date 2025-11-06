"""Domain exceptions for tickets"""


class InvalidTicketStatusError(Exception):
    """Raised when ticket status transition is invalid."""


class ClassificationError(Exception):
    """Raised when ticket classification fails."""


class RoutingError(Exception):
    """Raised when ticket routing fails."""
