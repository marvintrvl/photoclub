from django.db import models
from members.models import CustomUser
from datetime import date

class HomePageImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='home_page_images')
    image = models.ImageField(upload_to='home_page_images/')
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Image by {self.user.username}"

    @staticmethod
    def get_image_of_the_day():
        images = HomePageImage.objects.all()
        if images.exists():
            # Get the current day of the year to rotate images daily
            day_of_year = date.today().timetuple().tm_yday
            return images[day_of_year % images.count()]
        return None
