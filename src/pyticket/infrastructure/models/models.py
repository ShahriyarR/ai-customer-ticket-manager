"""Django models for tickets"""

from django.db import models
from django.utils import timezone


class TicketModel(models.Model):
    """Django model for Ticket entity"""

    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default="OPEN")
    category = models.CharField(max_length=20, null=True, blank=True)
    priority = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tickets"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"
