from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('members/', include('members.urls')),
    path('challenges/', include('challenges.urls')),
    path('meetups/', include('meetups.urls')),
]