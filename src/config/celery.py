import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_app = Celery("config")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.conf.timezone = "UTC"
# celery_app.conf.beat_schedule = {
#     "send_notifications": {
#         "task": "notifications.tasks.send_scheduled_notification_task",
#         "schedule": crontab(minute="*/1"),
#         # "args": (notification_id, recipient, subject, message),
#     },
# }

celery_app.autodiscover_tasks()


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
