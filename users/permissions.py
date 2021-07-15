from rest_framework.permissions import BasePermission

class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        if request.method == 'POST':
            return True
        return False