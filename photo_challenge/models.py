from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

class PhotoChallenge(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()
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

class PhotoChallengeSubmission(models.Model):
    challenge = models.ForeignKey(PhotoChallenge, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='challenge_submissions/')
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.challenge.name}"

class PhotoChallengeComment(models.Model):
    submission = models.ForeignKey(PhotoChallengeSubmission, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.submission.id}"

class PhotoChallengeVote(models.Model):
    submission = models.ForeignKey(PhotoChallengeSubmission, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('submission', 'user')

    def __str__(self):
        return f"Vote by {self.user.username} on {self.submission.id}"

    @staticmethod
    def user_vote_count(user, challenge):
        return PhotoChallengeVote.objects.filter(user=user, submission__challenge=challenge).count()

    @staticmethod
    def can_vote(user, submission):
        return PhotoChallengeVote.user_vote_count(user, submission.challenge) < 3 and not PhotoChallengeVote.objects.filter(user=user, submission=submission).exists()
