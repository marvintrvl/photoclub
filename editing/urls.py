from django.urls import path
from . import views

urlpatterns = [
    path('', views.editing_list, name='editing_list'),
    path('<int:editing_id>/', views.editing_detail, name='editing_detail'),
    path('edit/', views.editing_edit, name='editing_edit'),
]
