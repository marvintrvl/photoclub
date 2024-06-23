# editing/models.py
from django.db import models
from django.conf import settings

class EditingChallenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class EditingSubmission(models.Model):
    challenge = models.ForeignKey(EditingChallenge, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='editing_submissions/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Submission by {self.user.username} for {self.challenge.title}'
