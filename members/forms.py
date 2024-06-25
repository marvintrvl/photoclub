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
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserPhotoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = PhotoCategory.objects.filter(user=user)