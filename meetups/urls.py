# urls.py
from django.urls import path
from .views import meetup_list, meetup_detail, meetup_edit, meetup_list_private, meetup_create

urlpatterns = [
    path('', meetup_list, name='meetup_list'),
    path('<int:pk>/', meetup_detail, name='meetup_detail'),
    path('private/', meetup_list_private, name='meetup_list_private'),
    path('<int:pk>/edit/', meetup_edit, name='meetup_edit'),
    path('create/', meetup_create, name='meetup_create'),
]