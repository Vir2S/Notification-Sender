from celery import uuid
from django.db import models

from notifications.validators import validate_date
from users.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    scheduled_send_date = models.DateTimeField(validators=[validate_date])
    sent = models.BooleanField(default=False)
    task_id = models.CharField(max_length=50, default=str(uuid()))

    class Meta:
        db_table = "notifications"
        ordering = ("-scheduled_send_date", )

    def __str__(self):
        return f"{str(self.id)} Scheduled - {self.scheduled_send_date}"
