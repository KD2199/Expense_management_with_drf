
from rest_framework import permissions


class IsLoggedIn(permissions.BasePermission):
    """
    Object-level permission to only allow authenticate user to perform operations.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_logged_in and user.is_authenticated:
            return True


