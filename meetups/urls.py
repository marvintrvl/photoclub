from django.urls import path
from .views import meetup_list, meetup_detail, meetup_edit

app_name = 'meetups'

urlpatterns = [
    path('', meetup_list, name='meetup_list'),
    path('<int:pk>/', meetup_detail, name='meetup_detail'),
    path('edit/<int:pk>/', meetup_edit, name='meetup_edit'),
    path('edit/', meetup_edit, name='meetup_edit'),
]
