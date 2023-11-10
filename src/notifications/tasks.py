from config.celery import celery_app

from notifications.services import send_email


@celery_app.task
def send_scheduled_notification_task(instance: dict) -> str:
    print("Sending email...")
    send_email(
        subject=instance.get("subject"),
        message=instance.get("message"),
        recipient=instance.get("recipient")
    )
    print("Email has been sent")
    return "Email has been sent"
