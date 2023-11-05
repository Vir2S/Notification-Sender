from django.contrib import admin

from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "title",
        "scheduled_send_date"
    ]
    list_filter = ["scheduled_send_date", "user", "title", "id"]
    search_fields = ["title", "message", "scheduled_send_date", "user"]