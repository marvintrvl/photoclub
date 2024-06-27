from django.urls import path
from .views import (
    profile_edit, member_list, login_view, logout_view, member_detail,
    add_category, add_photo, delete_photo, delete_equipment, delete_interest,
    delete_photo_genre, add_equipment, add_interest, add_photo_genre,
    manage_steckbrief  # Make sure to import the manage_steckbrief view
)

app_name = 'members'

urlpatterns = [
    path('members/', member_list, name='member_list'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_edit, name='profile_edit'),
    path('profile/add_category/', add_category, name='add_category'),
    path('profile/add_photo/', add_photo, name='add_photo'),
    path('profile/delete_photo/<int:pk>/', delete_photo, name='delete_photo'),
    path('profile/delete_equipment/<int:pk>/', delete_equipment, name='delete_equipment'),
    path('profile/delete_interest/<int:pk>/', delete_interest, name='delete_interest'),
    path('profile/delete_photo_genre/<int:pk>/', delete_photo_genre, name='delete_photo_genre'),
    path('profile/add_equipment/', add_equipment, name='add_equipment'),
    path('profile/add_interest/', add_interest, name='add_interest'),
    path('profile/add_photo_genre/', add_photo_genre, name='add_photo_genre'),
    path('profile/manage_steckbrief/', manage_steckbrief, name='manage_steckbrief'),  # New URL for Steckbrief
    path('members/<str:username>/', member_detail, name='member_detail'),
]
