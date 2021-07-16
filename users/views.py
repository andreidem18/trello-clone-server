from .tasks import notification_email
from users.permissions import UserPermissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from users.serializer import MyUserSerializer, UpdateUserSerializer, UserSerializer, CreateUserSerializer
from users.serializer import UserSerializer
from .models import User

class UserViewSet(ModelViewSet):
    UserModel = User
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions, )

    def get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                data[k] = v
        return self.queryset.filter(**data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return super().get_serializer_class()



    def create(self, request, *args, **kwargs):
        notification_email.apply_async(
            args = [request.data["firstname"], request.data["email"]]
        )
        return super().create(request, *args, **kwargs)




    @action(methods = ['GET', 'DELETE', 'PUT', 'PATCH'], detail=False)
    def myself(self, request):
        if request.method == 'GET':
            serialized = MyUserSerializer(request.user)
            return Response(serialized.data)

        if request.method == 'DELETE':
            User.objects.get(id=request.user).delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

        if request.method == 'PUT':
            serialized = UpdateUserSerializer(data = request.data, instance=request.user)
            if not serialized.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST,data=serialized.errors)
            serialized.save()
            return Response(status = status.HTTP_200_OK, data = serialized.data)

        if request.method == 'PUT':
            serialized = UpdateUserSerializer(data = request.data, instance=request.user, partial=True)
            if not serialized.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST,data=serialized.errors)
            serialized.save()
            return Response(status = status.HTTP_200_OK, data = serialized.data)

#
