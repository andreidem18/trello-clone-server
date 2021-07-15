from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ItemChecklist
from .serializers import ItemSerializer
from users.models import User
from notifications.models import Notification
from .tasks import notification_email
from rest_framework.viewsets import ModelViewSet
from cards.models import Card

class ItemChecklistViewSet(ModelViewSet):
    queryset = ItemChecklist.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                data[k] = v
        return self.queryset.filter(**data)

    def create(self, request, *args, **kwargs):
        notify(request.user.firstname, request.data['task'], request.data["card"], request.data["responsibles"])
        return super().create(request, *args, **kwargs)




    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def responsibles(self, request, pk):
        item = self.get_object()

        if request.method == 'GET':
            return Response(
                status = status.HTTP_200_OK,
                data = item.responsibles.values()
            )


        if request.method == 'POST':
            data = request.data.copy()

            #To remove of request list the users who already were responsibles
            for responsible in list(item.responsibles.values()):
                for responsible_request in data["responsibles"]:
                    if str(responsible["id"]) == responsible_request:
                        data["responsibles"].remove(responsible_request)

            for user_id in data["responsibles"]:
                user = User.objects.get(id = user_id)
                item.responsibles.add(user)
            notify(request.user.firstname, item.task, item.card.id, data["responsibles"])
            return Response(status = status.HTTP_201_CREATED)


        if request.method == 'DELETE':
            for responsible_id in request.data["responsibles"]:
                user = User.objects.get(id=responsible_id)
                item.responsibles.remove(user)
            return Response(status = status.HTTP_204_NO_CONTENT)




def notify(user_name, task, card, responsibles):
    emails = []
    img = Card.objects.get(id=card).list.board.img_url
    for user_id in responsibles:
        user = User.objects.get(id=user_id)
        emails.append(user.email)
        Notification.objects.create(
            text = f"{user_name} have added you to a new task: {task}",
            url = '',
            img_url = img,
            user = user
        )    
        emails.append(user.email)
    notification_email.apply_async(
        args = [user_name, task, emails]
    )
