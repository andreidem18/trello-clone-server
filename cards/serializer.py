from rest_framework.serializers import ModelSerializer
from .models import Card

class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name', 'description', 'creator', "position", 'deadline', 'list')

class ModifyCardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name', 'description', 'deadline', 'list')
