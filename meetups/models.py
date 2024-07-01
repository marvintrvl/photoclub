from django.db import models
from django.utils import timezone
from members.models import CustomUser
from django.core.files.base import ContentFile
from PIL import Image
import io

def default_meetup_time():
    return timezone.now().time()

class Meetup(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255)
    detailed_description = models.TextField()
    date = models.DateField()
    time = models.TimeField(default=default_meetup_time)  # Set default using a function
    location = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(CustomUser, related_name='attending_meetups', blank=True)

    def __str__(self):
        return self.title

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
    
    # Further compress if still over 200KB
    if output.getbuffer().nbytes > 300 * 1024:
        quality = 85
        while output.getbuffer().nbytes > 300 * 1024 and quality > 10:
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            quality -= 5

    return ContentFile(output.getvalue(), name=image_field.name.split('.')[0] + '.jpg')

class MeetupImage(models.Model):
    meetup = models.ForeignKey(Meetup, related_name='images', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='meetup_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meetup_images/')

    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_and_compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Image for {self.meetup.title} by {self.user.username}'
