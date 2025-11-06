"""Django models module"""

from django.apps import AppConfig


class InfrastructureModelsConfig(AppConfig):
    """App config for infrastructure models"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "pyticket.infrastructure.models"
    verbose_name = "Infrastructure Models"
