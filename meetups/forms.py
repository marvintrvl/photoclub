from django import forms
from .models import Meetup

class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = ['title', 'short_description', 'detailed_description', 'date', 'location', 'topic']
