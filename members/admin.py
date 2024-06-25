from django.contrib import admin
from .models import CustomUser, PhotoCategory, UserPhoto

admin.site.register(CustomUser)
admin.site.register(PhotoCategory)
admin.site.register(UserPhoto)