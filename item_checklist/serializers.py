from .models import ItemChecklist
from rest_framework.serializers import ModelSerializer

class ItemSerializer(ModelSerializer):
    class Meta:
        model = ItemChecklist
        fields = ('id', 'task', 'responsibles', 'card')
