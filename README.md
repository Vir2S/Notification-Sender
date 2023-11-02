# Notification-Sender
Email notifications sender

## Description

The goal of the project is to create a simple service for sending notifications to users using Django, Celery, and PostgreSQL.
The service should allow the administrator to schedule and send notifications to users' emails.

### Models

    User: name, email.
    Notification: message text, scheduled send date.

### API

    Create a notification with a scheduled send date.
    View a list of scheduled notifications.

### Background Tasks
Using Celery, implement a task that will send notifications to users' emails at the scheduled time.

### Tests
Write unit tests to check the functionality of your application.


### Additional Requirements

    Implementation of the API using Django REST Framework.
    Use of Docker to simplify the deployment process.
    Push your code to GitHub.