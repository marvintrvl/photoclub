from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PhotoChallenge, PhotoChallengeSubmission, PhotoChallengeComment, PhotoChallengeVote
from .forms import PhotoChallengeForm, PhotoSubmissionForm, CommentForm
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from datetime import timedelta
from django.db import models
from django.db.models import Count

class PhotoChallengeListView(ListView):
    model = PhotoChallenge
    template_name = 'photo_challenge/photo_challenge_list.html'
    context_object_name = 'upcoming_challenges'

    def get_queryset(self):
        return PhotoChallenge.objects.filter(end_date__gte=timezone.now().date()).order_by('end_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['past_challenges'] = PhotoChallenge.objects.filter(end_date__lt=timezone.now().date()).order_by('-end_date')
        return context

class PhotoChallengeDetailView(DetailView):
    model = PhotoChallenge
    template_name = 'photo_challenge/photo_challenge_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenge = self.object
        submissions = challenge.submissions.all()

        submissions_with_comments = []
        for submission in submissions:
            user_picture = submission.user.picture.url if submission.user.picture else None
            has_voted = {
                1: submission.votes.filter(user=self.request.user, image_number=1).exists(),
                2: submission.votes.filter(user=self.request.user, image_number=2).exists(),
                3: submission.votes.filter(user=self.request.user, image_number=3).exists()
            } if self.request.user.is_authenticated else {1: False, 2: False, 3: False}
            
            vote_counts = submission.votes.values('image_number').annotate(count=Count('id'))
            vote_counts_dict = {vc['image_number']: vc['count'] for vc in vote_counts}

            
            comments = {
                1: list(submission.comments.filter(image_number=1, parent__isnull=True)),
                2: list(submission.comments.filter(image_number=2, parent__isnull=True)),
                3: list(submission.comments.filter(image_number=3, parent__isnull=True))
            }
            
            submissions_with_comments.append({
                'submission': submission,
                'comments': comments,
                'user_picture': user_picture,
                'has_voted': has_voted,
                'vote_counts': vote_counts_dict
            })

        context['submission_form'] = PhotoSubmissionForm(user=self.request.user, challenge=challenge)
        context['comment_form'] = CommentForm()
        context['submissions_with_comments'] = submissions_with_comments
        context['can_vote'] = challenge.end_date < timezone.now().date() <= challenge.voting_period_end
        context['user_votes_left'] = 3 - PhotoChallengeVote.user_vote_count(self.request.user, challenge) if self.request.user.is_authenticated else 0
        context['image_numbers'] = [1, 2, 3]
        return context

class PhotoChallengeCreateView(LoginRequiredMixin, CreateView):
    model = PhotoChallengeSubmission
    form_class = PhotoSubmissionForm
    template_name = 'photo_challenge/photo_challenge_detail.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['challenge'] = get_object_or_404(PhotoChallenge, id=self.kwargs['challenge_id'])
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(PhotoChallenge, id=self.kwargs['challenge_id'])
        if PhotoChallengeSubmission.objects.filter(user=request.user, challenge=self.challenge).exists():
            messages.success(request, "Du kannst nur 3 Fotos pro Challenge hochladen.")
            return redirect('photo_challenge:photo_challenge_detail', pk=self.kwargs['challenge_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.success(self.request, "Es gab ein Problem beim Hochladen deines Fotos. Bitte versuche es erneut.")
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.challenge = get_object_or_404(PhotoChallenge, id=self.kwargs['challenge_id'])
        response = super().form_valid(form)
        messages.success(self.request, "Dein Foto wurde erfolgreich hochgeladen.")
        return response

    def get_success_url(self):
        return reverse('photo_challenge:photo_challenge_detail', kwargs={'pk': self.kwargs['challenge_id']})

class PhotoChallengeUpdateView(LoginRequiredMixin, UpdateView):
    model = PhotoChallenge
    form_class = PhotoChallengeForm
    template_name = 'photo_challenge/photo_challenge_create.html'

    def get_success_url(self):
        return reverse('photo_challenge:photo_challenge_detail', kwargs={'pk': self.object.pk})

class PhotoSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = PhotoChallengeSubmission
    form_class = PhotoSubmissionForm
    template_name = 'photo_challenge/photo_challenge_detail.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['challenge'] = get_object_or_404(PhotoChallenge, id=self.kwargs['challenge_id'])
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        challenge = get_object_or_404(PhotoChallenge, id=self.kwargs['challenge_id'])
        if PhotoChallengeSubmission.objects.filter(user=request.user, challenge=challenge).exists():
            messages.success(request, "Du kannst nur 1 Beitrag pro Challenge hochladen.")
            return redirect('photo_challenge:photo_challenge_detail', pk=self.kwargs['challenge_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.success(self.request, "Es gab ein Problem beim Hochladen deines Fotos. Bitte versuche es erneut.")
        return super().form_invalid(form)

    def form_valid(self, form):
        print("Formulardaten:", form.cleaned_data)
        print("Challenge-ID aus der URL:", self.kwargs.get('challenge_id'))
        print("Benutzer:", self.request.user)
        
        form.instance.user = self.request.user
        form.instance.challenge = get_object_or_404(PhotoChallenge, id=self.kwargs['challenge_id'])
        
        print("Challenge dem Formular-Objekt zugewiesen:", form.instance.challenge)
        
        response = super().form_valid(form)
        messages.success(self.request, "Dein Foto wurde erfolgreich hochgeladen.")
        return response

    def get_success_url(self):
        return reverse('photo_challenge:photo_challenge_detail', kwargs={'pk': self.kwargs['challenge_id']})

def vote_submission(request, submission_id, image_number):
    submission = get_object_or_404(PhotoChallengeSubmission, id=submission_id)
    if not submission.challenge.voting_period_end >= timezone.now().date() > submission.challenge.end_date:
        raise PermissionDenied("Das Abstimmen ist außerhalb des Abstimmungszeitraums nicht erlaubt.")
    
    if PhotoChallengeVote.can_vote(request.user, submission, image_number):
        PhotoChallengeVote.objects.create(submission=submission, user=request.user, image_number=image_number)
    return redirect('photo_challenge:photo_challenge_detail', pk=submission.challenge.id)

def add_comment(request, submission_id, image_number):
    if request.method == 'POST':
        submission = get_object_or_404(PhotoChallengeSubmission, id=submission_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.submission = submission
            comment.image_number = image_number
            comment.save()
        else:
            print(f"Form errors: {form.errors}")  # Add this line for debugging
    return redirect('photo_challenge:photo_challenge_detail', pk=submission.challenge.id)

def determine_winner():
    now = timezone.now().date()
    challenges = PhotoChallenge.objects.filter(end_date__lt=now, end_date__gte=now - timedelta(days=7))
    for challenge in challenges:
        submissions = challenge.submissions.annotate(vote_count=models.Count('votes')).order_by('-vote_count')
        if submissions.exists() and not challenge.submissions.filter(is_winner=True).exists():
            submissions.first().is_winner = True
            submissions.first().save()

class PhotoChallengeEditListView(ListView):
    model = PhotoChallenge
    template_name = 'photo_challenge/photo_challenge_list_private.html'
    context_object_name = 'challenges'

    def get_queryset(self):
        return PhotoChallenge.objects.filter(created_by=self.request.user)
