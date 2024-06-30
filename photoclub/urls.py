from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('members.urls')),
    path('meetups/', include('meetups.urls')),
    path('editing/', include('editing_challenge.urls', namespace='editing_challenge')),
    path('photo/', include('photo_challenge.urls', namespace='photo_challenge')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)