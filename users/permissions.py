from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """
    Проверяет, входит ли пользователь в группу moderators.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="moderators").exists()
        )


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelf(permissions.BasePermission):
    """Разрешает изменять профиль только самому пользователю."""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.is_authenticated and obj == request.user
        )
