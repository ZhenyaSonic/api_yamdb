from rest_framework.permissions import BasePermission


class IsAdminWithToken(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_staff
                     or request.user.is_superuser))


class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff

    def has_create_permission(self, request, view):
        # Добавьте проверку на разрешение создания пользователя
        return (
            request.user and request.user.is_staff
            and request.user.has_perm('create_user_permission')
        )
