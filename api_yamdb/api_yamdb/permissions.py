from rest_framework.permissions import BasePermission


# class AdminOnlyPermission(BasePermission):
#     message = "Только администраторы имеют доступ к этому ресурсу."

#     def has_permission(self, request, view):
#         # Проверяем, является ли пользователь администратором
#         return (
#             request.user and request.user.is_authenticated
#             and request.user.role == 'admin'
#         )


class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff

    def has_create_permission(self, request, view):
        # Добавьте проверку на разрешение создания пользователя
        return request.user and request.user.is_staff and request.user.has_perm('create_user_permission')
