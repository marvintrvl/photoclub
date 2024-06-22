from django.urls import path
from .views import profile_detail, profile_edit, member_list

app_name = 'members'

urlpatterns = [
    path('', member_list, name='member_list'),
    path('profile/<str:username>/', profile_detail, name='profile_detail'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]
