from django.contrib.auth import get_user_model
from boards.models import Board
from django.db import models
from core.models import BaseModel

class Notification(BaseModel):
    text = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    img_url = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(
        get_user_model(),
        related_name='notifications',
        on_delete=models.SET_NULL,
        null = True
    )
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    
