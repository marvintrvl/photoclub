from django import forms
from .models import Meetup, MeetupImage

class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = ['title', 'short_description', 'detailed_description', 'date', 'time', 'location', 'topic']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'title': 'Titel',
            'short_description': 'Kurzbeschreibung',
            'detailed_description': 'Detaillierte Beschreibung',
            'date': 'Datum',
            'time': 'Uhrzeit',
            'location': 'Ort',
            'topic': 'Thema',
        }

class MeetupImageForm(forms.ModelForm):
    class Meta:
        model = MeetupImage
        fields = ['image']