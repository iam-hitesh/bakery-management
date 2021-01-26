from rest_framework import permissions


class AdminOnlyPermission(permissions.BasePermission):
    """
    Global permission check for staff user.
    """

    def has_permission(self, request, view):
        return request.user.is_staff
