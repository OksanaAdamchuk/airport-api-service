from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a admin user, or is a read-only request.
    """

    def has_permission(self, request, view) -> bool:
        return bool(
            request.method in SAFE_METHODS or (request.user and request.user.is_staff)
        )
