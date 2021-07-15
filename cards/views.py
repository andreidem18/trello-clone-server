from lists.models import List
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import CardSerializer, ModifyCardSerializer
from .models import Card
from rest_framework.viewsets import ModelViewSet
from .tasks import notificate_deadline

class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                data[k] = v
        return self.queryset.filter(**data)


    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ModifyCardSerializer
        return super().get_serializer_class()



    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["creator"] = request.user.id
        my_list = List.objects.get(id = data["list"])

        # To configure the default position
        positions = []
        for card in my_list.cards.all():
            positions.append(card.position)
        if positions:
            data["position"] = max(positions) + 1
        else:
            data["position"] = 1
        serialized = CardSerializer(data = data)

        if not serialized.is_valid():
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = serialized.errors
            )
        serialized.save()

        # To notify at the deadline of the card
        card = Card.objects.get(id = serialized.data["id"])
        members = card.list.board.members.values()
        img = card.list.board.img_url
        card.task_id = notificate_deadline.apply_async(
            args=[list(members), data["name"], img],
            eta = card.deadline
        )
        card.save()

        return Response(
            data = serialized.data,
            status = status.HTTP_201_CREATED
        )



    @action(methods = ['POST'], detail = True)
    def position(self, request, pk):

        # Algorithm to reorganizate all the positions when one of them changes
        card = Card.objects.get(id = pk)
        list = card.list
        current_position = card.position
        new_position = int(request.data["position"])
        max_value = max(current_position, new_position)
        min_value = min(current_position, new_position)
        id_next_card = ''
        while max_value > min_value:
            if current_position > new_position:
                max_value -= 1
                other_card = list.cards.get(position = max_value)
                other_card.position = max_value + 1
            else:
                if max_value == new_position:
                    other_card = list.cards.get(position = max_value)
                else:
                    other_card = list.cards.get(id = id_next_card)
                id_next_card = list.cards.get(position = max_value - 1).id
                other_card.position = max_value - 1
                max_value -= 1
            other_card.save()
        card.position = new_position
        card.save()
        return Response(status=status.HTTP_200_OK)



