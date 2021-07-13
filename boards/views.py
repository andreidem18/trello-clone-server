from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from notifications.serializer import NotificationSerializer
from boards.serializer import BoardSerializer, CreateBoardSerializer
from boards.models import Board
from .tasks import notification_email
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .permissions import BoardPermissions

class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (BoardPermissions,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateBoardSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                data[k] = v
        return self.queryset.filter(**data)

    def get_object(self):
        return get_object_or_404(Board, id=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().all()
        res = []
        for board in queryset:
            if board.is_public or request.user in board.members.all():
                res.append(board)
        serialized = BoardSerializer(res, many=True)
        return Response(serialized.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        data['creator'] = request.user.id
        data['members'].append(request.user.id)
        serialized = CreateBoardSerializer(data = data)
        if not serialized.is_valid():
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = serialized.errors
            )
        serialized.save()
        notify(data['members'], request.user, data['name'], data['img_url'])
        return Response(
            status = status.HTTP_201_CREATED,
            data = serialized.data
        )




    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def members(self, request, pk):
        board = self.get_object()

        if request.method == 'GET':
            return Response(
                status = status.HTTP_200_OK,
                data = board.members.values()
            )


        if request.method == 'POST':
            data = request.data.copy()

            #To remove of request list the users who already were in the board
            for member in list(board.members.values()):
                for member_request in data["members"]:
                    if str(member["id"]) == member_request:
                        data["members"].remove(member_request)

            for user_id in data["members"]:
                user = get_user_model().objects.get(id = user_id)
                board.members.add(user)
            notify(data["members"], request.user, board.name, board.img_url)
            return Response(status = status.HTTP_201_CREATED)


        if request.method == 'DELETE':
            for member_id in request.data["members"]:
                user = get_user_model().objects.get(id=member_id)
                board.members.remove(user)
            return Response(status = status.HTTP_204_NO_CONTENT)



        

    

def notify(members, user, board, img_url):
    emails = []
    UserModel = get_user_model()
    for member_id in members:
        user = UserModel.objects.get(id=member_id)
        emails.append(user.email)
        new_notification = {
            'text': f'{user.email} have added you to a new board: {board}',
            'url': '',
            'img_url': img_url,
            'user': member_id
        }
        serialized = NotificationSerializer(data = new_notification)
        if not serialized.is_valid():
            print(serialized.errors)
        serialized.save()
        email = user.email
        notification_email.apply_async(
            args = [email, board, emails]
        )