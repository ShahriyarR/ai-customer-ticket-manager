"""Ticket API endpoints"""

from typing import List
from uuid import UUID

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from pyticket.domain.tickets.entities import TicketStatus
from pyticket.entrypoints.web.api.dependencies import get_ticket_service
from pyticket.entrypoints.web.api.tickets.schemas import TicketCreateSchema, TicketResponseSchema, TicketUpdateStatusSchema
from pyticket.service.tickets.dtos import CreateTicketDTO

router = Router(tags=["tickets"])
auth = JWTAuth()


@router.post("/", response=TicketResponseSchema, auth=auth)
def create_ticket(request, payload: TicketCreateSchema):
    """Create and classify a ticket."""
    service = get_ticket_service()
    dto = CreateTicketDTO(title=payload.title, description=payload.description)
    ticket_dto = service.create_ticket(dto)

    return _to_response_schema(ticket_dto)


@router.get("/{ticket_id}", response=TicketResponseSchema, auth=auth)
def get_ticket(request, ticket_id: UUID):
    """Get a ticket by ID."""
    service = get_ticket_service()
    ticket_dto = service.get_ticket(ticket_id)

    if not ticket_dto:
        return {"error": "Ticket not found"}, 404

    return _to_response_schema(ticket_dto)


@router.get("/", response=List[TicketResponseSchema], auth=auth)
def list_tickets(request, limit: int = 100, offset: int = 0):
    """List tickets."""
    service = get_ticket_service()
    tickets = service.list_tickets(limit=limit, offset=offset)
    return [_to_response_schema(ticket) for ticket in tickets]


@router.post("/{ticket_id}/reclassify", response=TicketResponseSchema, auth=auth)
def reclassify_ticket(request, ticket_id: UUID):
    """Reclassify a ticket."""
    service = get_ticket_service()
    try:
        ticket_dto = service.reclassify_ticket(ticket_id)
        return _to_response_schema(ticket_dto)
    except ValueError as e:
        return {"error": str(e)}, 404


@router.patch("/{ticket_id}/status", response=TicketResponseSchema, auth=auth)
def update_ticket_status(request, ticket_id: UUID, payload: TicketUpdateStatusSchema):
    """Update ticket status."""
    service = get_ticket_service()
    try:
        new_status = TicketStatus(payload.status)
        ticket_dto = service.update_ticket_status(ticket_id, new_status)
        return _to_response_schema(ticket_dto)
    except ValueError as e:
        return {"error": f"Invalid status: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 400


def _to_response_schema(ticket_dto) -> dict:
    """Convert DTO to response schema."""
    from pyticket.entrypoints.web.api.tickets.schemas import ClassificationResultSchema

    classification = None
    if ticket_dto.classification:
        classification = ClassificationResultSchema(
            category=ticket_dto.classification.category.value,
            priority=ticket_dto.classification.priority.value,
            confidence_score=ticket_dto.classification.confidence_score,
            reasoning=ticket_dto.classification.reasoning,
        )

    return {
        "id": ticket_dto.id,
        "title": ticket_dto.title,
        "description": ticket_dto.description,
        "status": ticket_dto.status.value,
        "category": ticket_dto.category.value if ticket_dto.category else None,
        "priority": ticket_dto.priority.value if ticket_dto.priority else None,
        "created_at": ticket_dto.created_at,
        "updated_at": ticket_dto.updated_at,
        "classification": classification.dict() if classification else None,
    }
