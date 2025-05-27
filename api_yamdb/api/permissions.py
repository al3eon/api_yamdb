from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешает:
    - Чтение всем (включая анонимов)
    - Запись только администраторам (включая is_staff и is_superuser)
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_staff
                or request.user.is_superuser
            )
        )


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """Разрешает чтение всем, изменение - админам, модераторам или автору."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAdmin(BasePermission):
    """Только для администраторов (включая is_staff и is_superuser)."""

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_admin or user.is_staff or user.is_superuser
        )


class IsModerator(BasePermission):
    """Только для модераторов"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator
