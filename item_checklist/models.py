from users.models import User
from django.db import models
from cards.models import Card
from core.models import BaseModel

class ItemChecklist(BaseModel):
    task = models.CharField(max_length=200)
    done = models.BooleanField(default=False, null=True, blank=True)
    responsibles = models.ManyToManyField(
        User,
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

