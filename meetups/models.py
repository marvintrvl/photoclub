from django.db import models

class Meetup(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

class Meetup(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class MeetupImage(models.Model):
    meetup = models.ForeignKey(Meetup, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meetup_images/')

    def __str__(self):
        return f'Image for {self.meetup.title}'