from django.conf import settings
from django.db import models
from cards.models import Card
from core.models import BaseModel

class ItemChecklist(BaseModel):
    task = models.CharField(max_length=200)
    due_to = models.DateField()
    done = models.BooleanField()
    responsibles = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='tasks'
    )
    card = models.ForeignKey(
        Card,
        related_name='comments',
        on_delete=models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.task

