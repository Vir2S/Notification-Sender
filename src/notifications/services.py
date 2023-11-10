import smtplib

from django.conf import settings
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery.result import AsyncResult


def cancel_celery_task(task_id):
    try:
        result = AsyncResult(task_id)
        if result.state in ("PENDING", "RECEIVED", "STARTED"):
            result.revoke(terminate=True)
    except Exception as e:
        print(e)
        pass


def send_email(subject, message, recipient, attachment=None):
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    if attachment:
        with open(attachment, "rb") as file:
            part = MIMEApplication(file.read())
            part.add_header("Content-Disposition", "attachment", filename=attachment)
            msg.attach(part)

    try:
        smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
        smtp_conn.starttls()
        smtp_conn.login(smtp_user, smtp_password)
        smtp_conn.sendmail(smtp_user, recipient, msg.as_string())
        smtp_conn.quit()

        print("Hello from smtp :-)")
        return "Email has beem sent"

    except Exception as e:
        print(f"Bad news!")
        return f"Error: {str(e)}"
