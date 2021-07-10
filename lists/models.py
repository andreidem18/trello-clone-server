from boards.models import Board
from django.db import models
from core.models import BaseModel

class List(BaseModel):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(
        Board,
        related_name='lists',
        on_delete=models.SET_NULL,
        null=True
    )
    position = models.IntegerField()

    def __str__(self):
        return self.name
