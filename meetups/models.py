from django.db import models
from django.utils import timezone
from members.models import CustomUser

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

class MeetupImage(models.Model):
    meetup = models.ForeignKey(Meetup, related_name='images', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='meetup_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meetup_images/')

    def __str__(self):
        return f'Image for {self.meetup.title} by {self.user.username}'
