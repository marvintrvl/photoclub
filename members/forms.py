from django import forms
from .models import CustomUser, PhotoCategory, UserPhoto, Equipment, Interest, PhotoGenre, Steckbrief

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'description', 'picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
            'email': forms.EmailInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
            'picture': forms.FileInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['category', 'name']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'text-fgray-950 mb-2 block w-full mt-1',
            }),
            'name': forms.TextInput(attrs={
                'class': 'text-fgray-950 mb-2 block w-full mt-1',
            }),
        }

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
        }

class PhotoGenreForm(forms.ModelForm):
    class Meta:
        model = PhotoGenre
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
        }

class SteckbriefForm(forms.ModelForm):
    class Meta:
        model = Steckbrief
        fields = ['image_editing', 'preferred_shooting']
        widgets = {
            'image_editing': forms.CheckboxInput(attrs={'class': 'text-fgray-950 mb-2'}),
            'preferred_shooting': forms.Select(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}))

class PhotoCategoryForm(forms.ModelForm):
    class Meta:
        model = PhotoCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
        }

class UserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserPhoto
        fields = ['category', 'image', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
            'image': forms.FileInput(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'text-fgray-950 mb-2 block w-full'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserPhotoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = PhotoCategory.objects.filter(user=user)