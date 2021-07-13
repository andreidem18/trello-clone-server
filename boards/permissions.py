from rest_framework.permissions import BasePermission
from .models import Board

class BoardPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        print(obj)
        # if request.method in ['DELETE', 'UPDATE', 'PATCH']:
        #     board = Board.objects.get(id=view.get_object().id)
        #     if request.user != board.creator:
        #         return False
        #     if request.method == 'POST':
        #         return True
        return True

    def has_permission(self, request, view):
        if request.method in ['DELETE', 'UPDATE', 'PATCH']:
            board = Board.objects.get(id=view.get_object().id)
            if request.user != board.creator:
                return False
        return True