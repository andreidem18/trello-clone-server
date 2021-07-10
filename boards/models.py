from workspaces.models import Workspace
from django.db import models
from django.conf import settings
from workspaces.models import Workspace
from core.models import BaseModel

class Board(BaseModel):
    name = models.CharField(max_length=100)
    description  = models.TextField()
    img_url = models.CharField(max_length=200)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    favorite = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_boards'
    )
    is_public = models.BooleanField()
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='boards'
    )
    Workspace= models.ForeignKey(
        Workspace,
        related_name='boards',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name
