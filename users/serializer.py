from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'firstname', 'lastname')

class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'firstname', 'lastname')