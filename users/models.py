from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    location_preference = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
