import uuid
from django.db import models

class Ticket(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "RECEIVED"
        VALIDATED = "VALIDATED"
        ENRICHED = "ENRICHED"
        READY = "READY"
        FAILED = "FAILED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=50)
    external_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.RECEIVED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("source", "external_id")
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.source}:{self.external_id}"
