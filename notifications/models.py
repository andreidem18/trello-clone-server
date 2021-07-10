from django.conf import settings
from boards.models import Board
from django.db import models
from core.models import BaseModel

class Notification(BaseModel):
    text = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    board = models.ForeignKey(
        Board,
        related_name='activity',
        on_delete=models.SET_NULL,
        null = True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notifications',
        on_delete=models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.text

    
