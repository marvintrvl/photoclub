from django.contrib import admin
from .models import HomePageImage

# Register your models here.
@admin.register(HomePageImage)
class HomePageImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'upload_date', 'description')
    search_fields = ('user__username', 'description')