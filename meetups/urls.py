from django.urls import path
from .views import join_meetup, leave_meetup, delete_meetup, meetup_list, meetup_detail, meetup_edit, meetup_list_private, meetup_create, add_meetup_image, delete_meetup_image

urlpatterns = [
    path('', meetup_list, name='meetup_list'),
    path('<int:pk>/', meetup_detail, name='meetup_detail'),
    path('private/', meetup_list_private, name='meetup_list_private'),
    path('<int:pk>/edit/', meetup_edit, name='meetup_edit'),
    path('create/', meetup_create, name='meetup_create'),
    path('<int:meetup_id>/add_image/', add_meetup_image, name='add_meetup_image'),  # Add this line
    path('<int:meetup_id>/image/<int:image_id>/delete/', delete_meetup_image, name='meetup_image_delete'),
    path('delete/<int:pk>/', delete_meetup, name='delete_meetup'),
    path('<int:meetup_id>/join/', join_meetup, name='join_meetup'),
    path('<int:meetup_id>/leave/', leave_meetup, name='leave_meetup'),
]
