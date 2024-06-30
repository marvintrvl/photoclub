from django import forms
from .models import PhotoChallenge, PhotoChallengeSubmission, PhotoChallengeComment

class PhotoChallengeForm(forms.ModelForm):
    class Meta:
        model = PhotoChallenge
        fields = ['name', 'description', 'start_date', 'end_date']
        labels = {
            'name': 'Name',
            'description': 'Beschreibung',
            'start_date': 'Startdatum',
            'end_date': 'Enddatum',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PhotoSubmissionForm(forms.ModelForm):
    new_image = forms.ImageField(required=True)

    class Meta:
        model = PhotoChallengeSubmission
        fields = ['new_image']
        labels = {
            'new_image': 'Bild',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.challenge = kwargs.pop('challenge', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            submission = self.instance
            if submission.image1 and submission.image2 and submission.image3:
                raise forms.ValidationError("You cannot upload more than 3 images.")
        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = PhotoChallengeComment
        fields = ['text', 'parent', 'image_number']
        widgets = {
            'parent': forms.HiddenInput(),
            'image_number': forms.HiddenInput(),
        }