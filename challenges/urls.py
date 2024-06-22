from django.urls import path
from .views import challenge_list, challenge_detail, challenge_edit

app_name = 'challenges'

urlpatterns = [
    path('', challenge_list, name='challenge_list'),
    path('<int:pk>/', challenge_detail, name='challenge_detail'),
    path('edit/<int:pk>/', challenge_edit, name='challenge_edit'),
    path('edit/', challenge_edit, name='challenge_edit'),
]
