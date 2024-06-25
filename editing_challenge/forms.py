from django import forms
from .models import EditingChallenge, EditingChallengeSubmission, EditingChallengeComment

class EditingChallengeForm(forms.ModelForm):
    class Meta:
        model = EditingChallenge
        fields = ['name', 'details', 'start_date', 'end_date', 'raw_preview', 'raw_file']
        labels = {
            'name': 'Name',
            'details': 'Details',
            'start_date': 'Startdatum',
            'end_date': 'Enddatum',
            'raw_preview': 'Vorschau',
            'raw_file': 'Rohdatei',
        }

class EditingSubmissionForm(forms.ModelForm):
    class Meta:
        model = EditingChallengeSubmission
        fields = ['edited_image', 'description']
        labels = {
            'edited_image': 'Bearbeitetes Bild',
            'description': 'Beschreibung',
        }

    def clean_edited_image(self):
        user = self.instance.user
        challenge = self.instance.challenge
        if EditingChallengeSubmission.objects.filter(user=user, challenge=challenge).exists():
            raise forms.ValidationError("Du kannst nur 1 bearbeitetes Foto pro Challenge hochladen.")
        return self.cleaned_data.get('edited_image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = EditingChallengeComment
        fields = ['text', 'parent']
        labels = {
            'text': 'Text',
            'parent': 'Eltern',
        }
