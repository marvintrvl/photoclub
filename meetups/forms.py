from django import forms
from .models import Meetup

class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = ['title', 'short_description', 'detailed_description', 'date', 'time', 'location', 'topic']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }