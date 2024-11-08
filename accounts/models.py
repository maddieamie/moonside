from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    location = models.TextField(default="Seattle")
    name = models.TextField(default="Awesome Oppossum")
    profile_picture = models.CharField(max_length=255, default='moon_images/full.png')
    pass
 

    def __str__(self):
        return self.username
