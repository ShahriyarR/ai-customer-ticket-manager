"""Main API router for django-ninja"""

from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from pyticket.entrypoints.web.api.auth.endpoints import router as auth_router
from pyticket.entrypoints.web.api.exceptions import register_exception_handlers
from pyticket.entrypoints.web.api.tickets.router import router as tickets_router

api = NinjaExtraAPI(
    title="Customer Ticket Classifier API",
    version="1.0.0",
    description="AI-powered customer ticket classification system",
)

# Register exception handlers
register_exception_handlers(api)

# Register JWT controller (provides token refresh, verify endpoints)
api.register_controllers(NinjaJWTDefaultController)

# Register custom auth endpoints (register, login)
api.add_router("/auth", auth_router)

# Register ticket endpoints
api.add_router("/tickets", tickets_router)
