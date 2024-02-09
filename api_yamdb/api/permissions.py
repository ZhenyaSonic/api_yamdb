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


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author


class IsModeratorOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            ))
