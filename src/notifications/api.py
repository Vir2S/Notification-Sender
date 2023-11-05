from rest_framework import viewsets

from notifications.models import Notification
from notifications.permissions import RoleIsAdmin, RoleIsManager, RoleIsUser, IsOwner
from notifications.serializers import NotificationSerializer
from users.constants import Role


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == Role.ADMIN:
            return Notification.objects.all()

        return Notification.objects.filter(user=user)

    def get_permissions(self):
        match self.action:
            case "list":
                permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
            case "create":
                permission_classes = [RoleIsAdmin | RoleIsUser]
            case "retrieve":
                permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
            case "update":
                permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
            case "destroy":
                permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]