from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PhotoChallenge, PhotoChallengeSubmission, PhotoChallengeComment, PhotoChallengeVote
from .forms import PhotoChallengeForm, ChallengeSubmissionForm, CommentForm
from django.utils import timezone
from django.http import JsonResponse
from django.db import models
from datetime import timedelta
from django.urls import reverse
from django.contrib.auth.decorators import login_required

class PhotoChallengeListView(ListView):
    model = PhotoChallenge
    template_name = 'photo_challenge/photo_challenge_list.html'

class PhotoChallengeDetailView(DetailView):
    model = PhotoChallenge
    template_name = 'photo_challenge/photo_challenge_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission_form'] = ChallengeSubmissionForm()
        context['comment_form'] = CommentForm()
        return context

class PhotoChallengeCreateView(LoginRequiredMixin, CreateView):
    model = PhotoChallenge
    form_class = PhotoChallengeForm
    template_name = 'photo_challenge/photo_challenge_edit.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PhotoChallengeUpdateView(LoginRequiredMixin, UpdateView):
    model = PhotoChallenge
    form_class = PhotoChallengeForm
    template_name = 'photo_challenge/photo_challenge_edit.html'

class ChallengeSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = PhotoChallengeSubmission
    form_class = ChallengeSubmissionForm
    template_name = 'photo_challenge/challenge_submission_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.challenge = get_object_or_404(PhotoChallenge, id=self.kwargs['challenge_id'])
        return super().form_valid(form)

def vote_submission(request, submission_id):
    submission = get_object_or_404(PhotoChallengeSubmission, id=submission_id)
    if PhotoChallengeVote.can_vote(request.user, submission):
        PhotoChallengeVote.objects.create(submission=submission, user=request.user)
    return redirect('photo_challenge_detail', pk=submission.challenge.id)

def add_comment(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(PhotoChallengeSubmission, id=submission_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.submission = submission
            comment.save()
    return redirect('photo_challenge_detail', pk=submission.challenge.id)

def determine_winner():
    now = timezone.now().date()
    challenges = PhotoChallenge.objects.filter(end_date__lt=now, end_date__gte=now - timedelta(days=7))
    for challenge in challenges:
        submissions = challenge.submissions.annotate(vote_count=models.Count('votes')).order_by('-vote_count')
        if submissions.exists() and not challenge.submissions.filter(is_winner=True).exists():
            submissions.first().is_winner = True
            submissions.first().save()

class PhotoChallengeEditListView(LoginRequiredMixin, ListView):
    model = PhotoChallenge
    template_name = 'photo_challenge/photo_challenge_list_private.html'
    context_object_name = 'challenges'

    def get_queryset(self):
        return PhotoChallenge.objects.filter(created_by=self.request.user)
