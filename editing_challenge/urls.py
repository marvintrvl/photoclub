from django.urls import path
from . import views

app_name = 'editing_challenge'

urlpatterns = [
    path('', views.EditingChallengeListView.as_view(), name='editing_challenge_list'),
    path('challenge/<int:pk>/', views.EditingChallengeDetailView.as_view(), name='editing_challenge_detail'),
    path('challenge/new/', views.EditingChallengeCreateView.as_view(), name='editing_challenge_create'),  # Added URL
    path('challenge/edit/<int:pk>/', views.EditingChallengeUpdateView.as_view(), name='editing_challenge_edit'),
    path('submission/new/<int:challenge_id>/', views.EditingSubmissionCreateView.as_view(), name='editing_submission_create'),
    path('vote/<int:submission_id>/', views.vote_submission, name='editing_vote_submission'),
    path('comment/<int:submission_id>/', views.add_comment, name='editing_add_comment'),
    path('challenge/edit/list/', views.EditingChallengeEditListView.as_view(), name='editing_challenge_list_private'),
]
