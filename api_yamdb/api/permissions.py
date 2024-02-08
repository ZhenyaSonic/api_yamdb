from rest_framework.permissions import (SAFE_METHODS,
                                        BasePermission,
                                        IsAuthenticatedOrReadOnly)

ALLOWED_METHODS = ['PATCH', 'DELETE']


class IsMainAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_staff
                     or request.user.is_superuser))


class IsAdminOrReadOnly(BasePermission):
    """Разрешение на уровне админ."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAuthor(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author


class IsModerator(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class IsAdmin(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin
