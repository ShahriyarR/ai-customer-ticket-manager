"""OpenAI provider implementation"""

import json
import logging
from typing import Any, Dict

from django.conf import settings
from django_ai_assistant import AIAssistant

from pyticket.domain.tickets.entities import Category, Priority, Ticket
from pyticket.domain.tickets.exceptions import ClassificationError
from pyticket.infrastructure.ai.interfaces import AIClassificationService, ClassificationResult

logger = logging.getLogger(__name__)


class TicketClassificationAssistant(AIAssistant):
    """Django AI Assistant for ticket classification"""

    id = "ticket_classifier"
    name = "Ticket Classifier"
    instructions = """
    You are a customer support ticket classification system.
    Analyze the ticket title and description, then classify it into one of these categories:
    - TECHNICAL: Technical issues, bugs, system problems, login issues, API errors
    - BILLING: Payment, subscription, invoice issues, refund requests, payment failures
    - FEATURE_REQUEST: Requests for new features, enhancements, improvements
    - BUG_REPORT: Reports of software bugs, errors, unexpected behavior
    - GENERAL: General inquiries that don't fit other categories

    Also assign a priority:
    - LOW: Non-urgent, can wait, feature requests, general questions
    - MEDIUM: Standard priority, normal issues
    - HIGH: Important, needs attention soon, billing issues, login problems
    - URGENT: Critical, needs immediate attention, system down, payment blocked

    Respond with a JSON object containing:
    - category: one of the categories above
    - priority: one of the priorities above
    - confidence_score: a float between 0 and 1
    - reasoning: brief explanation of your classification

    Examples:

    Example 1:
    Title: Cannot log into my account
    Description: I've been trying to log in for the past hour but keep getting an error message saying "Invalid credentials" even though I'm using the correct password.
    Response: {"category": "TECHNICAL", "priority": "HIGH", "confidence_score": 0.95, "reasoning": "Login/authentication issue is a technical problem that needs prompt resolution"}

    Example 2:
    Title: Payment failed for my subscription
    Description: My credit card payment was declined when trying to renew my subscription. I need help resolving this immediately as my service will expire soon.
    Response: {"category": "BILLING", "priority": "HIGH", "confidence_score": 0.98, "reasoning": "Payment and subscription issue falls under billing category and is high priority"}

    Example 3:
    Title: Feature suggestion: Dark mode
    Description: It would be great if you could add a dark mode option to the application. Many users would appreciate this feature, especially for night-time usage.
    Response: {"category": "FEATURE_REQUEST", "priority": "LOW", "confidence_score": 0.92, "reasoning": "Request for new feature, not urgent"}

    Example 4:
    Title: Application crashes when uploading large files
    Description: Every time I try to upload a file larger than 100MB, the application crashes. This happens consistently on both Chrome and Firefox browsers.
    Response: {"category": "BUG_REPORT", "priority": "HIGH", "confidence_score": 0.96, "reasoning": "Report of reproducible software bug affecting functionality"}

    Example 5:
    Title: How do I export my data?
    Description: I would like to know how to export all my data from the platform. Is there a feature for this?
    Response: {"category": "GENERAL", "priority": "LOW", "confidence_score": 0.88, "reasoning": "General inquiry about platform features"}

    Example 6:
    Title: System is down - cannot access dashboard
    Description: The entire system appears to be down. I cannot access the dashboard, API is returning 500 errors, and none of my integrations are working. This is affecting our production environment.
    Response: {"category": "TECHNICAL", "priority": "URGENT", "confidence_score": 0.99, "reasoning": "System-wide outage is a critical technical issue requiring immediate attention"}
    """

    def get_model(self) -> str:
        """Get the model name from settings."""
        return getattr(settings, "AI_MODEL", "gpt-4o-mini")

    def get_temperature(self) -> float:
        """Get temperature setting."""
        return 0.3  # Lower temperature for more consistent classification


class OpenAIClassificationService(AIClassificationService):
    """OpenAI implementation of AI classification service"""

    def __init__(self):
        """Initialize OpenAI classification service."""
        self.assistant = TicketClassificationAssistant()
        api_key = getattr(settings, "OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured")

    def classify_ticket(self, ticket: Ticket) -> ClassificationResult:
        """Classify ticket using OpenAI."""
        try:
            prompt = f"Title: {ticket.title}\n\nDescription: {ticket.description}"
            response = self.assistant.run(prompt)

            # Convert response to string if needed
            if not isinstance(response, str):
                response = str(response)

            # Parse JSON response
            result = self._parse_response(response)

            # Map to domain entities
            category = Category(result["category"])
            priority = Priority(result["priority"])
            confidence = float(result["confidence_score"])
            reasoning = result["reasoning"]

            logger.info(f"Classified ticket {ticket.id}: {category.value}, {priority.value}, " f"confidence: {confidence}")

            return ClassificationResult(
                category=category,
                priority=priority,
                confidence_score=confidence,
                reasoning=reasoning,
            )
        except Exception as e:
            logger.error(f"OpenAI classification failed for ticket {ticket.id}: {e}")
            raise ClassificationError(f"Failed to classify ticket: {str(e)}") from e

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured data."""
        # Try to extract JSON from response
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON object
            import re

            json_match = re.search(r"\{[^{}]*\}", response)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"Could not parse response as JSON: {response}")
