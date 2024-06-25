from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EditingChallenge, EditingChallengeSubmission, EditingChallengeComment, EditingChallengeVote
from .forms import EditingChallengeForm, EditingSubmissionForm, CommentForm
from django.utils import timezone
from django.http import JsonResponse
from django.db import models
from datetime import timedelta
from django.urls import reverse

class EditingChallengeListView(ListView):
    model = EditingChallenge
    template_name = 'editing_challenge/editing_challenge_list.html'

class EditingChallengeDetailView(DetailView):
    model = EditingChallenge
    template_name = 'editing_challenge/editing_challenge_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenge = self.object
        submissions = challenge.submissions.all()

        # Create a list of submissions with their comments
        submissions_with_comments = []
        for submission in submissions:
            submissions_with_comments.append({
                'submission': submission,
                'comments': submission.comments.filter(parent__isnull=True)
            })

        context['submission_form'] = EditingSubmissionForm()
        context['comment_form'] = CommentForm()
        context['submissions_with_comments'] = submissions_with_comments

        return context

class EditingChallengeCreateView(LoginRequiredMixin, CreateView):
    model = EditingChallenge
    form_class = EditingChallengeForm
    template_name = 'editing_challenge/editing_challenge_edit.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EditingChallengeUpdateView(LoginRequiredMixin, UpdateView):
    model = EditingChallenge
    form_class = EditingChallengeForm
    template_name = 'editing_challenge/editing_challenge_edit.html'

class EditingSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = EditingChallengeSubmission
    form_class = EditingSubmissionForm
    template_name = 'editing_challenge/editing_submission_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.challenge = get_object_or_404(EditingChallenge, id=self.kwargs['challenge_id'])
        return super().form_valid(form)

def vote_submission(request, submission_id):
    submission = get_object_or_404(EditingChallengeSubmission, id=submission_id)
    if EditingChallengeVote.can_vote(request.user, submission):
        EditingChallengeVote.objects.create(submission=submission, user=request.user)
    return redirect('editing_challenge_detail', pk=submission.challenge.id)

def add_comment(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(EditingChallengeSubmission, id=submission_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.submission = submission
            comment.save()
    return redirect('editing_challenge_detail', pk=submission.challenge.id)

def determine_winner():
    now = timezone.now().date()
    challenges = EditingChallenge.objects.filter(end_date__lt=now, end_date__gte=now - timedelta(days=7))
    for challenge in challenges:
        submissions = challenge.submissions.annotate(vote_count=models.Count('votes')).order_by('-vote_count')
        if submissions.exists() and not challenge.submissions.filter(is_winner=True).exists():
            submissions.first().is_winner = True
            submissions.first().save()

class EditingChallengeEditListView(ListView):
    model = EditingChallenge
    template_name = 'editing_challenge/editing_challenge_list_private.html'
    context_object_name = 'challenges'

    def get_queryset(self):
        return EditingChallenge.objects.filter(created_by=self.request.user)
