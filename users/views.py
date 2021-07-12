from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.serializer import UserSerializer, CreateUserSerializer
from users.serializer import UserSerializer
from django.contrib.auth import get_user_model

class UserViewSet(ModelViewSet):
    UserModel = get_user_model()
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        user = self.UserModel.objects.create_user(
            username = '',
            password = request.data['password'],
            email = request.data['email']
        )
        user.firstname = request.data['firstname']
        user.lastname = request.data['lastname']
        serialized = UserSerializer(user)
        return Response(
            status = status.HTTP_201_CREATED,
            data = serialized
        )


