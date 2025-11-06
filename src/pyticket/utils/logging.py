"""Logging configuration"""

import logging
import sys
from typing import Any

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Get logger for this module
logger = logging.getLogger(__name__)


def log_ai_request(
    ticket_id: str,
    provider: str,
    model: str,
    prompt_length: int,
    **kwargs: Any,
) -> None:
    """Log AI classification request."""
    logger.info(
        f"AI Request - Ticket: {ticket_id}, Provider: {provider}, " f"Model: {model}, Prompt Length: {prompt_length}",
        extra={"ticket_id": ticket_id, "provider": provider, "model": model},
    )


def log_ai_response(
    ticket_id: str,
    provider: str,
    category: str,
    priority: str,
    confidence: float,
    response_time: float,
    **kwargs: Any,
) -> None:
    """Log AI classification response."""
    logger.info(
        f"AI Response - Ticket: {ticket_id}, Provider: {provider}, "
        f"Category: {category}, Priority: {priority}, "
        f"Confidence: {confidence:.2f}, Response Time: {response_time:.2f}s",
        extra={
            "ticket_id": ticket_id,
            "provider": provider,
            "category": category,
            "priority": priority,
            "confidence": confidence,
            "response_time": response_time,
        },
    )


def log_ai_error(
    ticket_id: str,
    provider: str,
    error: Exception,
    **kwargs: Any,
) -> None:
    """Log AI classification error."""
    logger.error(
        f"AI Error - Ticket: {ticket_id}, Provider: {provider}, " f"Error: {str(error)}",
        extra={"ticket_id": ticket_id, "provider": provider, "error": str(error)},
        exc_info=True,
    )


def log_ticket_operation(
    operation: str,
    ticket_id: str,
    **kwargs: Any,
) -> None:
    """Log ticket operation."""
    logger.info(
        f"Ticket Operation - {operation}, Ticket: {ticket_id}",
        extra={"operation": operation, "ticket_id": ticket_id, **kwargs},
    )
