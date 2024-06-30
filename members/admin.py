from django.contrib import admin
from .models import CustomUser, PhotoCategory, UserPhoto, Equipment, Interest, PhotoGenre, Steckbrief

admin.site.register(CustomUser)
admin.site.register(PhotoCategory)
admin.site.register(UserPhoto)
admin.site.register(Equipment)
admin.site.register(Interest)
admin.site.register(PhotoGenre)
admin.site.register(Steckbrief)