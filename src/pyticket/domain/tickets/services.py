"""Domain services for tickets"""

from pyticket.domain.tickets.entities import Category, Priority


class TicketClassificationService:
    """Domain service for ticket classification rules"""

    @staticmethod
    def validate_classification(category: Category, priority: Priority) -> bool:
        """Validate classification combination."""
        # Business rule: URGENT priority should not be used with GENERAL category
        if priority == Priority.URGENT and category == Category.GENERAL:
            return False
        return True

    @staticmethod
    def get_default_priority_for_category(category: Category) -> Priority:
        """Get default priority based on category."""
        defaults = {
            Category.TECHNICAL: Priority.MEDIUM,
            Category.BILLING: Priority.HIGH,
            Category.FEATURE_REQUEST: Priority.LOW,
            Category.BUG_REPORT: Priority.HIGH,
            Category.GENERAL: Priority.LOW,
        }
        return defaults.get(category, Priority.MEDIUM)


class TicketRoutingService:
    """Domain service for ticket routing rules"""

    @staticmethod
    def get_team_for_category(category: Category) -> str:
        """Get team name for category."""
        routing_map = {
            Category.TECHNICAL: "technical-support",
            Category.BILLING: "billing-team",
            Category.FEATURE_REQUEST: "product-team",
            Category.BUG_REPORT: "engineering-team",
            Category.GENERAL: "customer-support",
        }
        return routing_map.get(category, "customer-support")
