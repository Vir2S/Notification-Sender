from celery import uuid
from rest_framework import serializers

from notifications.models import Notification
from notifications.validators import validate_date


class NotificationSerializer(serializers.ModelSerializer):
    scheduled_send_date = serializers.DateTimeField(validators=[validate_date], required=True)
    task_id = serializers.CharField(default=str(uuid()), read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["created_at", "sent", "task_id"]
        required_fields = ["user", "scheduled_send_date", "message"]
