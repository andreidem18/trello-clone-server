from rest_framework.serializers import ModelSerializer
from users.models import User
from .models import Board

class UserSerializerOnlyName(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", 'firstname')

class BoardSerializer(ModelSerializer):
    members = UserSerializerOnlyName(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ("id", "name", "description", "img_url", "creator", "favorite", "is_public", "members", "workspace", "created_at")

class CreateBoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ("id", "name", "description", "img_url", "creator", "is_public", "members", "workspace")
