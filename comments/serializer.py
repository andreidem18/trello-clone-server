from .models import Comment
from rest_framework.serializers import ModelSerializer

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'creator', 'text', 'card', 'created_at')
