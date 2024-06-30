from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

class Equipment(models.Model):
    CATEGORIES = [
        ('camera', 'Kamera'),
        ('lens', 'Objektive'),
        ('filter', 'Filter'),
        ('accessory', 'Sonstiges Zubehör'),
    ]
    user = models.ForeignKey(CustomUser, related_name='equipment', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"

class Interest(models.Model):
    user = models.ForeignKey(CustomUser, related_name='interests', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class PhotoGenre(models.Model):
    user = models.ForeignKey(CustomUser, related_name='photo_genres', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Steckbrief(models.Model):
    user = models.OneToOneField(CustomUser, related_name='steckbrief', on_delete=models.CASCADE)
    image_editing = models.BooleanField(verbose_name="What do you think about image editing?", default=False)
    preferred_shooting = models.CharField(
        max_length=100,
        choices=[('alone', 'Alone'), ('group', 'In a group')],
        verbose_name="Do you prefer shooting alone or in a group?",
        default='alone'
    )
    # Add more fields as needed


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