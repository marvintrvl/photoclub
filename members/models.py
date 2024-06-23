from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    equipment = models.TextField()
    interests = models.TextField()
    description = models.TextField()
    picture = models.ImageField(upload_to='profiles/', blank=True, null=True)