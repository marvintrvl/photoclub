from django.urls import path
from . import views

app_name = 'photo_challenge'

urlpatterns = [
    path('', views.PhotoChallengeListView.as_view(), name='photo_challenge_list'),
    path('challenge/<int:pk>/', views.PhotoChallengeDetailView.as_view(), name='photo_challenge_detail'),
    path('challenge/new/', views.PhotoChallengeCreateView.as_view(), name='photo_challenge_create'),
    path('challenge/edit/<int:pk>/', views.PhotoChallengeUpdateView.as_view(), name='photo_challenge_edit'),
    path('submission/new/<int:challenge_id>/', views.PhotoSubmissionCreateView.as_view(), name='photo_submission_create'),
    path('vote/<int:submission_id>/', views.vote_submission, name='photo_vote_submission'),
    path('comment/<int:submission_id>/', views.add_comment, name='photo_add_comment'),
    path('challenge/edit/list/', views.PhotoChallengeEditListView.as_view(), name='photo_challenge_list_private'),
]
