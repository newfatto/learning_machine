from rest_framework.permissions import BasePermission


class IsModer(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderators').exists():
            return True

        return False

