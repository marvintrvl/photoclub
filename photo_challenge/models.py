from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.files.base import ContentFile
from PIL import Image
import io
import os

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

    # Generate a new filename
    original_name = os.path.basename(image_field.name)
    name, ext = os.path.splitext(original_name)
    
    # Remove any existing '_resized' suffixes
    name = name.rsplit('_resized', 1)[0]
    
    new_name = f"{name}_resized.jpg"

    return ContentFile(output.getvalue(), name=new_name)

class PhotoChallenge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date.day != 1 or self.end_date != self.start_date.replace(day=1) + timedelta(days=30):
            raise ValidationError("Challenges must start on the 1st and end on the last day of the month.")

    @property
    def voting_period_end(self):
        return self.end_date + timedelta(days=7)

    def get_absolute_url(self):
        return reverse('photo_challenge:photo_challenge_detail', kwargs={'pk': self.pk})


class PhotoChallengeSubmission(models.Model):
    challenge = models.ForeignKey(PhotoChallenge, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='photo_submissions')
    image2 = models.ImageField(upload_to='photo_submissions', blank=True, null=True)
    image3 = models.ImageField(upload_to='photo_submissions', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.challenge.name}"

    def save(self, *args, **kwargs):
        if self.image1 and not self.image1.name.endswith('_resized.jpg'):
            self.image1 = resize_and_compress_image(self.image1)
        if self.image2 and not self.image2.name.endswith('_resized.jpg'):
            self.image2 = resize_and_compress_image(self.image2)
        if self.image3 and not self.image3.name.endswith('_resized.jpg'):
            self.image3 = resize_and_compress_image(self.image3)
        super().save(*args, **kwargs)

class PhotoChallengeComment(models.Model):
    submission = models.ForeignKey(PhotoChallengeSubmission, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    image_number = models.IntegerField(choices=[(1, 'Image 1'), (2, 'Image 2'), (3, 'Image 3')])

    def __str__(self):
        return f"Comment by {self.user.username} on {self.submission.id} (Image {self.image_number})"

class PhotoChallengeVote(models.Model):
    submission = models.ForeignKey(PhotoChallengeSubmission, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image_number = models.IntegerField(choices=[(1, 'Image 1'), (2, 'Image 2'), (3, 'Image 3')])

    class Meta:
        unique_together = ('submission', 'user', 'image_number')

    def __str__(self):
        return f"Vote by {self.user.username} on {self.submission.id} (Image {self.image_number})"

    @staticmethod
    def user_vote_count(user, challenge):
        return PhotoChallengeVote.objects.filter(user=user, submission__challenge=challenge).count()

    @staticmethod
    def can_vote(user, submission, image_number):
        return (
            PhotoChallengeVote.user_vote_count(user, submission.challenge) < 3
            and not PhotoChallengeVote.objects.filter(user=user, submission=submission, image_number=image_number).exists()
        )