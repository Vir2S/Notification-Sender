from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    scheduled_send_date = serializers.DateTimeField()

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["created_at", "sent"]
