from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    """Разрешение только на чтение"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
