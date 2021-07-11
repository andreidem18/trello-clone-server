from django.contrib.auth import get_user_model
from django.db import models
from cards.models import Card
from core.models import BaseModel

class ItemChecklist(BaseModel):
    task = models.CharField(max_length=200)
    due_to = models.DateField()
    done = models.BooleanField()
    responsibles = models.ManyToManyField(
        get_user_model(),
        related_name='tasks'
    )
    card = models.ForeignKey(
        Card,
        related_name='items_checklist',
        on_delete=models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.task

