from users.models import User
from cards.models import Card
from django.db import models
from core.models import BaseModel

class Comment(BaseModel):
    text = models.TextField()
    creator = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.SET_NULL,
        null = True
    )
    card = models.ForeignKey(
        Card,
        related_name='comments',
        on_delete=models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.creator