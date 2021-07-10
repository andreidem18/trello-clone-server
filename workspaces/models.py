from django.db import models
from django.conf import settings
from core.models import BaseModel

class Workspace(BaseModel):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    img_url = models.CharField(max_length=200)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='workspaces'
    )

    def __str__(self):
        return self.name
