from celery import uuid
from rest_framework import status, viewsets
from rest_framework.response import Response

from notifications.models import Notification
from notifications.permissions import RoleIsAdmin, RoleIsManager, RoleIsUser, IsOwner
from notifications.serializers import NotificationSerializer
from notifications.services import cancel_celery_task
from notifications.tasks import send_scheduled_notification_task
from users.constants import Role


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Notification.objects.none()

        if user.role == Role.ADMIN or user.role == Role.MANAGER:
            return Notification.objects.all()

        return Notification.objects.filter(user=user)

    def get_permissions(self):
        match self.action:
            case "list":
                permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
            case "create":
                permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
            case "retrieve":
                permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
            case "update":
                permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
            case "destroy":
                permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == Role.ADMIN or user.role == Role.MANAGER:
            instance = serializer.save()

        else:
            if user != serializer.validated_data.get("user") or user.is_anonymous:
                return Response(
                    {
                        "error": "You don't have permission to create",
                    },
                    status=403,
                )

            instance = serializer.save(user=user)

        recipient = instance.user.email
        subject = instance.title
        message = instance.message
        scheduled_time = instance.scheduled_send_date
        task_id = instance.task_id

        instance_to_task = {
            "id": instance.id,
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "scheduled_time": scheduled_time,
        }

        send_scheduled_notification_task.apply_async(
            (instance_to_task,), task_id=task_id, eta=scheduled_time
        )

    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        if user.is_anonymous or (
            user != instance.user and user.role not in [Role.ADMIN, Role.MANAGER]
        ):
            return Response(
                {
                    "error": "You don't have permission to update this notification",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            instance, data=request.data, partial=kwargs.pop("partial", False)
        )
        serializer.is_valid(raise_exception=True)

        old_task_id = instance.task_id
        instance.task_id = str(uuid())
        new_task_id = instance.task_id

        if instance.sent:
            instance.sent = False

        updated_instance = serializer.save()

        cancel_celery_task(old_task_id)

        recipient = updated_instance.user.email
        subject = updated_instance.title
        message = updated_instance.message
        scheduled_time = updated_instance.scheduled_send_date

        instance_to_task = {
            "id": instance.id,
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "scheduled_time": scheduled_time,
        }

        send_scheduled_notification_task.apply_async(
            (instance_to_task,), task_id=new_task_id, eta=scheduled_time
        )

        headers = self.get_success_headers(serializer.data)

        return Response(
            data=serializer.data, status=200, headers=headers
        )
