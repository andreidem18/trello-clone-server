from rest_framework.serializers import ModelSerializer
from django.conf import settings

class UserSerializer(ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('username', 'email', 'firstname', 'lastname')

class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('email', 'password', 'firstname', 'lastname')