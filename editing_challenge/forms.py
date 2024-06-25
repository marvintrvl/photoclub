from django import forms
from .models import EditingChallenge, EditingChallengeSubmission, EditingChallengeComment

class EditingChallengeForm(forms.ModelForm):
    class Meta:
        model = EditingChallenge
        fields = ['name', 'details', 'start_date', 'end_date', 'raw_preview', 'raw_file']

class EditingSubmissionForm(forms.ModelForm):
    class Meta:
        model = EditingChallengeSubmission
        fields = ['edited_image', 'description']

    def clean_edited_image(self):
        user = self.instance.user
        challenge = self.instance.challenge
        if EditingChallengeSubmission.objects.filter(user=user, challenge=challenge).exists():
            raise forms.ValidationError("You can only upload 1 edited photo per challenge.")
        return self.cleaned_data.get('edited_image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = EditingChallengeComment
        fields = ['text', 'parent']
