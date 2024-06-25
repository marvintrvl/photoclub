from django import forms
from .models import PhotoChallenge, PhotoChallengeSubmission, PhotoChallengeComment

class PhotoChallengeForm(forms.ModelForm):
    class Meta:
        model = PhotoChallenge
        fields = ['name', 'details', 'start_date', 'end_date']

class ChallengeSubmissionForm(forms.ModelForm):
    class Meta:
        model = PhotoChallengeSubmission
        fields = ['image', 'description']

    def clean_image(self):
        user = self.instance.user
        challenge = self.instance.challenge
        if PhotoChallengeSubmission.objects.filter(user=user, challenge=challenge).count() >= 3:
            raise forms.ValidationError("You can only upload up to 3 photos per challenge.")
        return self.cleaned_data.get('image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = PhotoChallengeComment
        fields = ['text', 'parent']
