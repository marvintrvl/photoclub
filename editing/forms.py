# editing/forms.py
from django import forms
from .models import EditingSubmission

class EditingSubmissionForm(forms.ModelForm):
    class Meta:
        model = EditingSubmission
        fields = ['challenge', 'image', 'caption']
