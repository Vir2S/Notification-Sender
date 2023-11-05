from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from users.constants import Role

from notifications.models import Notification


User = get_user_model()


def user_authenticated(user):
    if isinstance(user, AnonymousUser):
        raise PermissionDenied("Forbidden")


class RoleIsAdmin(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.ADMIN


class RoleIsManager(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.MANAGER


class RoleIsUser(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return request.user.role == Role.USER


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user_authenticated(user=request.user)
        return True

    def has_object_permission(self, request, view, obj: Notification):
        return obj.user == request.user
