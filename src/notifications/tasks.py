from celery import shared_task
from django.utils import timezone
from .models import Notification


@shared_task
def send_scheduled_notifications():
    current_time = timezone.now()
    notifications_to_send = Notification.objects.filter(
        scheduled_send_date__lte=current_time,
        sent=False
    )

    for notification in notifications_to_send:
        # TODO: Implement email's sending logic
        notification.sent = True
        notification.save()
