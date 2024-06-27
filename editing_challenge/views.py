from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EditingChallenge, EditingChallengeSubmission, EditingChallengeComment, EditingChallengeVote
from .forms import EditingChallengeForm, EditingSubmissionForm, CommentForm
from django.utils import timezone
from django.http import JsonResponse
from django.db import models
from datetime import timedelta
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from members.models import CustomUser
from django.contrib import messages


class EditingChallengeListView(ListView):
    model = EditingChallenge
    template_name = 'editing_challenge/editing_challenge_list.html'
    context_object_name = 'upcoming_challenges'  # This will be used for upcoming challenges

    def get_queryset(self):
        # This queryset now specifically fetches upcoming challenges
        return EditingChallenge.objects.filter(end_date__gte=timezone.now().date()).order_by('end_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add past challenges to the context
        context['past_challenges'] = EditingChallenge.objects.filter(end_date__lt=timezone.now().date()).order_by('-end_date')
        return context

class EditingChallengeDetailView(DetailView):
    model = EditingChallenge
    template_name = 'editing_challenge/editing_challenge_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenge = self.object
        submissions = challenge.submissions.all()

        # Create a list of submissions with their comments and voting status
        submissions_with_comments = []
        for submission in submissions:
            user_picture = submission.user.picture.url if submission.user.picture else None
            has_voted = submission.votes.filter(user=self.request.user).exists() if self.request.user.is_authenticated else False
            submissions_with_comments.append({
                'submission': submission,
                'comments': submission.comments.filter(parent__isnull=True),
                'user_picture': user_picture,
                'has_voted': has_voted
            })

        context['submission_form'] = EditingSubmissionForm()
        context['comment_form'] = CommentForm()
        context['submissions_with_comments'] = submissions_with_comments
        context['can_vote'] = challenge.end_date < timezone.now().date() <= challenge.voting_period_end

        return context


class EditingChallengeCreateView(LoginRequiredMixin, CreateView):
    model = EditingChallenge
    form_class = EditingChallengeForm
    template_name = 'editing_challenge/editing_challenge_create.html'
    success_url = reverse_lazy('editing_challenge:editing_challenge_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EditingChallengeUpdateView(LoginRequiredMixin, UpdateView):
    model = EditingChallenge
    form_class = EditingChallengeForm
    template_name = 'editing_challenge/editing_challenge_create.html'

class EditingSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = EditingChallengeSubmission
    form_class = EditingSubmissionForm
    template_name = 'editing_challenge/editing_challenge_detail.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['challenge'] = get_object_or_404(EditingChallenge, id=self.kwargs['challenge_id'])
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(EditingChallenge, id=self.kwargs['challenge_id'])
        if EditingChallengeSubmission.objects.filter(user=request.user, challenge=self.challenge).exists():
            messages.error(request, "Du hast bereits ein Foto für diese Challenge hochgeladen.")
            return redirect('editing_challenge:editing_challenge_detail', pk=self.challenge.id)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.challenge = get_object_or_404(EditingChallenge, id=self.kwargs['challenge_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('editing_challenge:editing_challenge_detail', kwargs={'pk': self.kwargs['challenge_id']})

def vote_submission(request, submission_id):
    submission = get_object_or_404(EditingChallengeSubmission, id=submission_id)
    if not submission.challenge.voting_period_end >= timezone.now().date() > submission.challenge.end_date:
        raise PermissionDenied("Voting is not allowed outside the voting period.")
    
    if EditingChallengeVote.can_vote(request.user, submission):
        EditingChallengeVote.objects.create(submission=submission, user=request.user)
    return redirect('editing_challenge:editing_challenge_detail', pk=submission.challenge.id)

def add_comment(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(EditingChallengeSubmission, id=submission_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.submission = submission
            comment.save()
    return redirect('editing_challenge:editing_challenge_detail', pk=submission.challenge.id)

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
