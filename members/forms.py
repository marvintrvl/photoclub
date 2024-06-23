from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'equipment', 'interests', 'description', 'picture']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)