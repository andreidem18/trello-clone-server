from rest_framework.serializers import ModelSerializer
from .models import List

class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'board', 'position')


class ModifyListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'board')