"""Exception handlers for django-ninja API"""

from django.http import JsonResponse
from ninja import NinjaAPI

from pyticket.domain.tickets.exceptions import ClassificationError, InvalidTicketStatusError, RoutingError


def register_exception_handlers(api: NinjaAPI) -> None:
    """Register custom exception handlers."""

    @api.exception_handler(InvalidTicketStatusError)
    def invalid_ticket_status_handler(request, exc):
        return JsonResponse({"error": str(exc)}, status=400)

    @api.exception_handler(ClassificationError)
    def classification_error_handler(request, exc):
        return JsonResponse({"error": str(exc)}, status=500)

    @api.exception_handler(RoutingError)
    def routing_error_handler(request, exc):
        return JsonResponse({"error": str(exc)}, status=500)
