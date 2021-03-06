from .models import Notification
from rest_framework.serializers import ModelSerializer

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ('text', 'url', 'img_url', 'user')

class GetNotificationsSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'text', 'url', 'img_url', 'seen')

