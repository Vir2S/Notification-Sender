from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from notifications.models import Notification


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
    subject = "Welcome to Paradise"
    message = "Hi! I'm glad to see you at my home!"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["virtualik@gmail.com"]
    # send_mail(
    #     subject=subject,
    #     message=message,
    #     from_email=email_from,
    #     recipient_list=recipient_list
    # )
    print("Mail has been sent")
    return "Mail has been sent"
