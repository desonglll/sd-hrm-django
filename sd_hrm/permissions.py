from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    仅管理员可写，其他人只读。
    """

    def has_permission(self, request, view):
        # SAFE_METHODS 包括 GET、HEAD、OPTIONS
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff
