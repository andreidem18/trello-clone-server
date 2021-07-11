from django.contrib.auth import get_user_model
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
        get_user_model(),
        related_name='notifications',
        on_delete=models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.text

    
