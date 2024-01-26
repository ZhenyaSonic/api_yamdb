from rest_framework.permissions import BasePermission


class AdminOnlyPermission(BasePermission):
    message = "Только администраторы имеют доступ к этому ресурсу."

    def has_permission(self, request, view):
        # Проверяем, является ли пользователь администратором
        return request.user and request.user.is_authenticated and request.user.role == 'admin'