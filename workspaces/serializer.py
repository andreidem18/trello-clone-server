from rest_framework.serializers import ModelSerializer
from .models import Workspace

class WorkspaceSerializer(ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('id', 'name', 'type', 'img_url', 'members', 'owner')
