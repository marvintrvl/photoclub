from django import forms
from .models import Meetup, MeetupImage

class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields = ['title', 'short_description', 'detailed_description', 'date', 'time', 'location', 'topic', 'google_maps_link']
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
            'google_maps_link': 'Google Maps Link',
        }

class MeetupImageForm(forms.ModelForm):
    class Meta:
        model = MeetupImage
        fields = ['image']