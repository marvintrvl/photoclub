from django import forms
from .models import PhotoChallenge, PhotoChallengeSubmission, PhotoChallengeComment

class PhotoChallengeForm(forms.ModelForm):
    class Meta:
        model = PhotoChallenge
        fields = ['name', 'description', 'start_date', 'end_date']
        labels = {
            'name': 'Name',
            'description': 'Beschreibung',
            'start_date': 'Ende',
            'end_date': 'End Date',
        }

class PhotoSubmissionForm(forms.ModelForm):
    class Meta:
        model = PhotoChallengeSubmission
        fields = ['image1', 'image2', 'image3']
        labels = {
            'image1': 'Bild 1',
            'image2': 'Bild 2',
            'image3': 'Bild 3',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.challenge = kwargs.pop('challenge', None)
        super().__init__(*args, **kwargs)
        print("Form initialized with user:", self.user)
        print("Form initialized with challenge:", self.challenge)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.challenge:
            instance.challenge = self.challenge
        if commit:
            instance.save()
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = PhotoChallengeComment
        fields = ['text', 'parent']
        labels = {
            'text': 'Text',
            'parent': 'Parent',
        }
