from django.conf import settings
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    task = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    logo = models.BinaryField(null=True, blank=True)
    logo_content_type = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return f"{self.task}"
