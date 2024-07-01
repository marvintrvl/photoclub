from django.db import models
from members.models import CustomUser
from datetime import date
from django.core.files.base import ContentFile
from PIL import Image
import io

def resize_and_compress_image(image_field, target_pixels=3000000, max_file_size=300*1024):
    img = Image.open(image_field)
    
    # Convert to RGB if it's not
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Calculate new size
    width, height = img.size
    aspect_ratio = width / height
    new_width = int((target_pixels * aspect_ratio) ** 0.5)
    new_height = int(target_pixels / new_width)
    
    # Resize
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Compress
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=85, optimize=True)
    output.seek(0)
    
    # Further compress if still over max_file_size
    if output.getbuffer().nbytes > max_file_size:
        quality = 85
        while output.getbuffer().nbytes > max_file_size and quality > 10:
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            quality -= 5

    return ContentFile(output.getvalue(), name=image_field.name.split('.')[0] + '.jpg')

class HomePageImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='home_page_images')
    image = models.ImageField(upload_to='home_page_images/')
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Image by {self.user.username}"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_and_compress_image(self.image)
        super().save(*args, **kwargs)

    @staticmethod
    def get_image_of_the_day():
        images = HomePageImage.objects.all()
        if images.exists():
            # Get the current day of the year to rotate images daily
            day_of_year = date.today().timetuple().tm_yday
            return images[day_of_year % images.count()]
        return None