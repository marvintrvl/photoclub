from django.urls import path
from .views import profile_edit, member_list, login_view, logout_view, member_detail, add_category, add_photo, delete_photo

app_name = 'members'

urlpatterns = [
    path('members', member_list, name='member_list'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_edit, name='profile_edit'),
    path('profile/add_category/', add_category, name='add_category'),
    path('profile/add_photo/', add_photo, name='add_photo'),
    path('profile/delete_photo/<int:pk>/', delete_photo, name='delete_photo'),
    path('members/<str:username>/', member_detail, name='member_detail'),
]
