from django.urls import path
from .views import profile_edit, member_list, login_view, logout_view, member_detail

app_name = 'members'

urlpatterns = [
    path('members', member_list, name='member_list'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_edit, name='profile_edit'),
    path('members/<str:username>/', member_detail, name='member_detail'),  # Correct this line
]
