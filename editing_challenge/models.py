from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.urls import reverse
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

class EditingChallenge(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    raw_preview = models.ImageField(upload_to='raw_previews/')
    raw_file = models.FileField(upload_to='raw_files/')

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date.day != 1 or self.end_date != self.start_date.replace(day=1) + timedelta(days=30):
            raise ValidationError("Challenges must start on the 1st and end on the last day of the month.")

    @property
    def voting_period_end(self):
        return self.end_date + timedelta(days=7)
    
    def get_absolute_url(self):
        return reverse('editing_challenge:editing_challenge_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.raw_preview:
            self.raw_preview = resize_and_compress_image(self.raw_preview)
        super().save(*args, **kwargs)

class EditingChallengeSubmission(models.Model):
    challenge = models.ForeignKey(EditingChallenge, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    edited_image = models.ImageField(upload_to='edited_submissions/')
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.challenge.name}"

    def save(self, *args, **kwargs):
        if self.edited_image:
            self.edited_image = resize_and_compress_image(self.edited_image)
        super().save(*args, **kwargs)

class EditingChallengeComment(models.Model):
    submission = models.ForeignKey(EditingChallengeSubmission, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.submission.id}"

class EditingChallengeVote(models.Model):
    submission = models.ForeignKey(EditingChallengeSubmission, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('submission', 'user')

    def __str__(self):
        return f"Vote by {self.user.username} on {self.submission.id}"

    @staticmethod
    def user_vote_count(user, challenge):
        return EditingChallengeVote.objects.filter(user=user, submission__challenge=challenge).count()

    @staticmethod
    def can_vote(user, submission):
        return EditingChallengeVote.user_vote_count(user, submission.challenge) < 3 and not EditingChallengeVote.objects.filter(user=user, submission=submission).exists()
