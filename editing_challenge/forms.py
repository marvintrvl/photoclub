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
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'raw_preview': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'raw_file': forms.ClearableFileInput(),
        }

class EditingSubmissionForm(forms.ModelForm):
    class Meta:
        model = EditingChallengeSubmission
        fields = ['edited_image']
        labels = {
            'edited_image': 'Bearbeitetes Bild',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.challenge = kwargs.pop('challenge', None)
        super().__init__(*args, **kwargs)

    def clean_edited_image(self):
        if EditingChallengeSubmission.objects.filter(user=self.user, challenge=self.challenge).exists():
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
