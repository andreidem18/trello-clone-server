from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel

class User(AbstractUser, BaseModel):
    def __str___(self):
        return self.username
