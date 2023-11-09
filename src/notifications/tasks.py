from celery import shared_task
from django.conf import settings
from django.utils import timezone

from notifications.models import Notification
from notifications.services import send_email


# @shared_task
# def send_scheduled_notification_task():
#     current_time = timezone.now()
#     notifications_to_send = Notification.objects.filter(
#         scheduled_send_date__lte=current_time,
#         sent=False
#     )
#
#     for notification in notifications_to_send:
#         # TODO: Implement email's sending logic
#         # notification.sent = True
#         print(f"{notification} -- Notification Sent")
#         # notification.save()

@shared_task
def send_scheduled_notification_task():
    print("Sending email...")
    send_email(subject, message, [recipient])
    print("Email has been sent")
    return "Email has been sent"
