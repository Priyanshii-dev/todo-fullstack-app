from rest_framework.permissions import BasePermission
from .models import User


class IsAdmin(BasePermission):
    message = "Admin access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role   == User.Role.ADMIN      # ← must be admin
            and request.user.status == User.Status.APPROVED  # ← must be approved
        )


class IsEmployee(BasePermission):
    message = "Employee access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role   == User.Role.EMPLOYEE
            and request.user.status == User.Status.APPROVED
        )


class IsApprovedUser(BasePermission):
    message = "Your account is pending approval or has been rejected."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.status == User.Status.APPROVED
        )