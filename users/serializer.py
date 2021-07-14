from rest_framework.serializers import ModelSerializer
from notifications.serializer import GetNotificationsSerializer
from workspaces.models import Workspace
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname')

class WorkspaceToUsersSerializer(ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('id', 'name', 'img_url')

class MyUserSerializer(ModelSerializer):
    notifications = GetNotificationsSerializer(read_only=True, many=True)
    workspaces = WorkspaceToUsersSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname', 'notifications', 'workspaces')


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'firstname', 'lastname')


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname')