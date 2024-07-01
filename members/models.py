from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
import io

def resize_and_compress_image(image_field):
    img = Image.open(image_field)
    
    # Convert to RGB if it's not
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Calculate new size
    width, height = img.size
    target_pixels = 3000000  # 3 million pixels
    aspect_ratio = width / height
    new_width = int((target_pixels * aspect_ratio) ** 0.5)
    new_height = int(target_pixels / new_width)
    
    # Resize
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Compress
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=85, optimize=True)
    output.seek(0)
    
    # Further compress if still over 300KB
    if output.getbuffer().nbytes > 300 * 1024:
        quality = 85
        while output.getbuffer().nbytes > 300 * 1024 and quality > 10:
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            quality -= 5

    return ContentFile(output.getvalue(), name=image_field.name.split('.')[0] + '.jpg')

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.picture:
            self.picture = resize_and_compress_image(self.picture)
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_and_compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Photo by {self.user.username} in {self.category.name}"