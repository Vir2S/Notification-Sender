from config.celery import celery_app

from notifications.services import mark_as_sent, send_email


@celery_app.task
def send_scheduled_notification_task(instance: dict) -> str:
    print("Sending email...")
    send_email(
        subject=instance.get("subject"),
        message=instance.get("message"),
        recipient=instance.get("recipient")
    )
    print("Email has been sent")
    mark_as_sent(notification_id=instance.get("id"))
    return "Email has been sent"
