from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "notifications"
        ordering = ("-id", )

    def __str__(self):
        return self.title
