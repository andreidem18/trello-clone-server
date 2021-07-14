from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from boards.models import Board
from lists.serializer import ListSerializer, ModifyListSerializer
from lists.models import List
from rest_framework.viewsets import ModelViewSet

class ListViewSet(ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                data[k] = v
        return self.queryset.filter(**data)


    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ModifyListSerializer
        return super().get_serializer_class()



    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        #To configure the default position
        board = Board.objects.get(id = data["board"])
        positions = []
        for list in board.lists.all():
            positions.append(list.position)
        data["position"] = max(positions) + 1
        serialized = ListSerializer(data = data)

        if not serialized.is_valid():
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = serialized.errors
            )
        serialized.save()
        return Response(
            data = serialized.data,
            status = status.HTTP_201_CREATED
        )



    @action(methods = ['POST'], detail = True)
    def position(self, request, pk):
        # Algorithm to reorganizate all the position when one of the list change it
        my_list = List.objects.get(id = pk)
        board = Board.objects.get(id = my_list.board.id)
        current_position = my_list.position
        new_position = int(request.data["position"])
        max_value = max(current_position, new_position)
        min_value = min(current_position, new_position)
        id_next_list = ''
        while max_value > min_value:
            if current_position > new_position:
                max_value -= 1
                other_list = board.lists.get(position = max_value)
                other_list.position = max_value + 1
            else:
                if max_value == new_position:
                    other_list = board.lists.get(position = max_value)
                else:
                    other_list = board.lists.get(id = id_next_list)
                id_next_list = board.lists.get(position = max_value - 1).id
                other_list.position = max_value - 1
                max_value -= 1
            other_list.save()
        my_list.position = new_position
        my_list.save()
        return Response(status=status.HTTP_200_OK)

