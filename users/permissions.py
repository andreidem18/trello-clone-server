from rest_framework.permissions import BasePermission

class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        if request.user.is_authenticated:
            return True
        return False