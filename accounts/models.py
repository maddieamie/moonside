from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    location = models.TextField(default="Seattle")
    name = models.TextField(default="Awesome Oppossum")
    pass
 

    def __str__(self):
        return self.username
