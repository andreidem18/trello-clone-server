from django.conf import settings
from lists.models import List
from django.db import models

from core.models import BaseModel

class Card(BaseModel):
    name = models.CharField(max_length=100)
    list = models.ForeignKey(
        List,
        related_name='cards',
        on_delete=models.SET_NULL,
        null=True
    )
    description = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    deadline = models.DateTimeField()
    position = models.IntegerField()

    def __str__(self):
        return self.name
