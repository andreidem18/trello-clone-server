from cards.models import Card
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Comment
from notifications.models import Notification
from .serializer import CommentSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                data[k] = v
        return self.queryset.filter(**data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["creator"] = request.user.id
        serialized = CommentSerializer(data = data)
        if not serialized.is_valid():
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = serialized.errors
            )
        serialized.save()

        # To get the users with tasks from the card to notify them
        card = Card.objects.get(id = data['card'])
        users = [card.creator]
        for item in card.items_checklist.all():
            for user in item.responsibles.all():
                users.append(user)
        users = list(set(users))
        notify(request.user, card.name, data['text'], users, card.list.board.img_url)

        return Response(
            status = status.HTTP_201_CREATED,
            data = serialized.data
        )


def notify(user_name, card, comment, recivers, img):
    for user in recivers:
        Notification.objects.create(
            text = f"{user_name} commented in {card}: {comment[:20]}...",
            url = '',
            img_url = img,
            user = user
        )    

