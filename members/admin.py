from django.contrib import admin
from .models import CustomUser, PhotoCategory, UserPhoto, Equipment, Interest, PhotoGenre, Steckbrief
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'full_name', 'description', 'picture')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name', 'description', 'picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'description', 'picture', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)

    def has_add_permission(self, request):
        # Only allow superusers to add new users
        return request.user.is_superuser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PhotoCategory)
admin.site.register(UserPhoto)
admin.site.register(Equipment)
admin.site.register(Interest)
admin.site.register(PhotoGenre)
admin.site.register(Steckbrief)