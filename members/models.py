from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    equipment = models.TextField()
    interests = models.TextField()
    description = models.TextField()
    picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

class PhotoCategory(models.Model):
    user = models.ForeignKey(CustomUser, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserPhoto(models.Model):
    user = models.ForeignKey(CustomUser, related_name='photos', on_delete=models.CASCADE)
    category = models.ForeignKey(PhotoCategory, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_photos/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Photo by {self.user.username} in {self.category.name}"
