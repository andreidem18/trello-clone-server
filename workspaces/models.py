from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel

class Workspace(BaseModel):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    img_url = models.CharField(max_length=200)
    members = models.ManyToManyField(
        get_user_model(),
        related_name='workspaces'
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete = models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.name
