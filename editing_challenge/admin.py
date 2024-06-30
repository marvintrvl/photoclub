from django.contrib import admin
from .models import EditingChallenge, EditingChallengeSubmission, EditingChallengeComment, EditingChallengeVote

# Register your models here.
admin.site.register(EditingChallenge)
admin.site.register(EditingChallengeSubmission)
admin.site.register(EditingChallengeComment)
admin.site.register(EditingChallengeVote)