from django.contrib import admin
from .models import PhotoChallenge, PhotoChallengeSubmission, PhotoChallengeComment, PhotoChallengeVote

admin.site.register(PhotoChallenge)
admin.site.register(PhotoChallengeSubmission)
admin.site.register(PhotoChallengeComment)
admin.site.register(PhotoChallengeVote)
