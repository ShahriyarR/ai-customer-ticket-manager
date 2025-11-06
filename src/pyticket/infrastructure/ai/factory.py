"""Factory for creating AI classification services"""

import logging

from django.conf import settings

from pyticket.infrastructure.ai.interfaces import AIClassificationService
from pyticket.infrastructure.ai.providers.anthropic_provider import AnthropicClassificationService
from pyticket.infrastructure.ai.providers.openai_provider import OpenAIClassificationService

logger = logging.getLogger(__name__)


class AIClassificationServiceFactory:
    """Factory for creating AI classification service instances"""

    @staticmethod
    def create() -> AIClassificationService:
        """
        Create an AI classification service based on configuration.

        Returns:
            An instance of AIClassificationService

        Raises:
            ValueError: If provider is not configured or not supported
        """
        provider = getattr(settings, "AI_PROVIDER", "OPENAI").upper()

        if provider == "OPENAI":
            logger.info("Creating OpenAI classification service")
            return OpenAIClassificationService()
        elif provider == "ANTHROPIC":
            logger.info("Creating Anthropic classification service")
            return AnthropicClassificationService()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}. " f"Supported providers: OPENAI, ANTHROPIC")
