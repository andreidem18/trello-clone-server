from rest_framework.permissions import BasePermission
from .models import Workspace

class WorkspacePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['DELETE', 'UPDATE', 'PATCH']:
            workspace = Workspace.objects.get(id=view.get_object().id)
            if request.user != workspace.owner:
                return False
        return True