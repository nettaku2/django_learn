from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(request.user)
        print(bool(request.user and request.user.is_staff))
        return bool(request.user and request.user.is_staff)
