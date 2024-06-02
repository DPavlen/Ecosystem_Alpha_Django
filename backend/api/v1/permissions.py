from rest_framework import permissions


class IsOwnerOrReadOnlyOrAdmin(permissions.BasePermission):
    """
    Пользователь может редактировать только свои собственные объекты.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить любые запросы на чтение.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить редактирование объекта только автору.
        return (
            request.user.is_authenticated
            and obj.user == request.user
            or request.user.is_staff
        )
