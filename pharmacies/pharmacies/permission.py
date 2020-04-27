from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """
    The request is authenticated as an admin
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class IsStaff(permissions.BasePermission):
    """
    The request is authenticated as a member of a staff
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as an admin, or is a read-only request
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a member of a staff, or is a read-only request
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_staff:
            return True
        else:
            return False


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True
        else:
            return False
