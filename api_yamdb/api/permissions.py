from rest_framework.permissions import SAFE_METHODS, BasePermission

ALLOWED_METHODS = ['PATCH', 'DELETE']


class IsAdmin(BasePermission):

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


class ReviewCommentPermissions(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ALLOWED_METHODS:
            if request.user == obj.author:
                return True

            if request.user.is_moderator:
                return True

            if request.user.is_admin:
                return True

        return request.method in SAFE_METHODS


class IsAuthenticatedMixin(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)


class IsAuthor(IsAuthenticatedMixin):

    def has_object_permission(self, request, view, obj):
        if request.method in ALLOWED_METHODS:
            if request.user == obj.author:
                return True

        return request.method in SAFE_METHODS


class IsModerator(IsAuthenticatedMixin):

    def has_object_permission(self, request, view, obj):
        if request.method in ALLOWED_METHODS:
            return ((request.user.is_authenticated and request.user.is_moderator))
        return request.method in SAFE_METHODS

    # def has_object_permission(self, request, view, obj):
    #     if request.method in ALLOWED_METHODS:
    #         if request.user.is_moderator:
    #             return True
    #     return request.method in SAFE_METHODS


class IsAdm(IsAuthenticatedMixin):

    def has_object_permission(self, request, view, obj):
        if request.method in ALLOWED_METHODS:
            return (request.user.is_authenticated and request.user.is_admin)
        return request.method in SAFE_METHODS
    

class AdminModer(BasePermission):
    def has_permission(self, request, view):
        if request.method in ALLOWED_METHODS:
            if request.user.is_moderator:
                return True
            
            if request.user.is_admin:
                return True
            
            return request.method in SAFE_METHODS


# class Agjasd(BasePermission):
#     def has_permission(self, request, view):
#         return (request.method in SAFE_METHODS
#                 or request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         if request.method in ALLOWED_METHODS:
#             if IsModerator().has_permission(request, view):
#                 return True

#             if IsAdmin().has_permission(request, view):
#                 return True

#         return request.method in SAFE_METHODS

    # def has_object_permission(self, request, view, obj):
    #     if request.method in ALLOWED_METHODS:
    #         if request.user.is_admin:
    #             return True
    #     return request.method in SAFE_METHODS


# class IsAuthor(BasePermission):
#     def has_permission(self, request, view):
#         return (request.method in SAFE_METHODS
#                 or request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         if request.method in ALLOWED_METHODS:
#             return request.user == obj.author
#         return request.method in SAFE_METHODS


# class IsModerator(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ALLOWED_METHODS:
#             return request.user.is_moderator
#         return request.method in SAFE_METHODS


# class IsAdm(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ALLOWED_METHODS:
#             return request.user.is_admin
#         return request.method in SAFE_METHODS
