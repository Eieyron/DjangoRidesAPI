# app/permissions.py
from rest_framework import permissions
from djangoRideAPI import settings

class IsRoleAdmin(permissions.BasePermission):
    """
    Global permission: allows access only to admin role users.
    """
    def has_permission(self, request, view):
        user = request.user

        # allow public endpoints
        if any(request.path.startswith(url) for url in settings.PUBLIC_ENDPOINTS):
            return True

        return bool(
            user and
            user.is_authenticated and
            getattr(user, 'role') == 'admin'
        )
