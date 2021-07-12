from rest_framework.serializers import ModelSerializer
from .models import Board

class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ("name", "description", "img_url", "creator", "favorite", "is_public", "members", "workspace")

class CreateBoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ("name", "description", "img_url", "is_public", "members", "workspace")
# name
# description
# img_url
# creator
# favorite
# is_public
# members
# Workspace