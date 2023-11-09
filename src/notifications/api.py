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

        send_scheduled_notification_task.apply_async(
            args=(
                instance.id,
                recipient,
                subject,
                message,
                scheduled_time
            ),
            eta=scheduled_time
        )

    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance

        if user.is_anonymous or (
            user != instance.user
            and user.role != Role.ADMIN
            and user.role != Role.MANAGER
        ):
            return Response(
                {
                    "error": "You don't have permission to update this object",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer.save()

        send_scheduled_notification_task.delay(instance.id)

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_anonymous or (
            user != instance.user and user.role not in [Role.ADMIN, Role.MANAGER]
        ):
            return Response(
                {
                    "error": "You don't have permission to delete this object",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        cancel_celery_task(instance.celery_task_id)

        instance.delete()
