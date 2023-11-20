from celery import uuid
from django.shortcuts import get_object_or_404
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
                permission_classes = [RoleIsAdmin | RoleIsManager | IsOwner]
            case "update":
                permission_classes = [RoleIsAdmin | RoleIsManager | IsOwner]
            case "destroy":
                permission_classes = [RoleIsAdmin | RoleIsManager | IsOwner]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == Role.ADMIN or user.role == Role.MANAGER:
            notification = serializer.save()

        else:
            if user != serializer.validated_data.get("user") or user.is_anonymous:
                return Response(
                    {
                        "error": "You don't have permission to create",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            notification = serializer.save(user=user)

        scheduled_time = notification.scheduled_send_date
        task_id = notification.task_id

        notification_to_task = {
            "id": notification.id,
            "recipient": notification.user.email,
            "subject": notification.title,
            "message": notification.message,
            "scheduled_time": scheduled_time,
        }

        send_scheduled_notification_task.apply_async(
            (notification_to_task,), task_id=task_id, eta=scheduled_time
        )

    def update(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=request.data.get("id"))

        serializer = self.get_serializer(
            notification, data=request.data, partial=kwargs.pop("partial", False)
        )
        serializer.is_valid(raise_exception=True)

        old_task_id = notification.task_id
        notification.task_id = str(uuid())
        new_task_id = notification.task_id

        if notification.sent:
            notification.sent = False

        updated_notification = serializer.save()

        cancel_celery_task(old_task_id)

        scheduled_time = updated_notification.scheduled_send_date

        notification_to_task = {
            "id": notification.id,
            "recipient": updated_notification.user.email,
            "subject": updated_notification.title,
            "message": updated_notification.message,
            "scheduled_time": scheduled_time,
        }

        send_scheduled_notification_task.apply_async(
            (notification_to_task,), task_id=new_task_id, eta=scheduled_time
        )

        headers = self.get_success_headers(serializer.data)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def delete(self, request):
        notification = get_object_or_404(Notification, pk=request.data.get("id"))

        task_id = notification.task_id
        cancel_celery_task(task_id)
        self.perform_destroy(notification)

        return Response(
            {"detail": "Notification successfully deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )
