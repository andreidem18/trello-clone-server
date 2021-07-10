from django.db import models
from uuid import uuid4

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
