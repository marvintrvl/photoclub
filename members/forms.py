from django import forms
from .models import CustomUser, PhotoCategory, UserPhoto

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'equipment', 'interests', 'description', 'picture']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class PhotoCategoryForm(forms.ModelForm):
    class Meta:
        model = PhotoCategory
        fields = ['name']

class UserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserPhoto
        fields = ['category', 'image', 'description']