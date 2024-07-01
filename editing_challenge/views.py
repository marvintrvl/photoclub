import os
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EditingChallenge, EditingChallengeSubmission, EditingChallengeComment, EditingChallengeVote
from .forms import EditingChallengeForm, EditingSubmissionForm, CommentForm
from django.utils import timezone
from django.db import models
from datetime import timedelta
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from members.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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

@login_required
def editing_challenge_edit(request, pk):
    challenge = get_object_or_404(EditingChallenge, pk=pk)
    if request.method == 'POST':
        form_data = request.POST.copy()
        if not form_data.get('start_date'):
            form_data['start_date'] = challenge.start_date
        if not form_data.get('end_date'):
            form_data['end_date'] = challenge.end_date

        form = EditingChallengeForm(form_data, request.FILES, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, "Die Editing Challenge wurde erfolgreich aktualisiert.")
            if 'raw_preview' in request.FILES:
                messages.info(request, "Eine neue Vorschau-Datei wurde hochgeladen.")
            if 'raw_file' in request.FILES:
                messages.info(request, "Eine neue Rohdatei wurde hochgeladen.")
            return redirect(reverse('editing_challenge:editing_challenge_detail', kwargs={'pk': challenge.pk}))
        else:
            print("Form is not valid:", form.errors)
    else:
        form = EditingChallengeForm(instance=challenge)
    return render(request, 'editing_challenge/editing_challenge_edit.html', {'form': form, 'challenge': challenge})

@login_required
def delete_editing_challenge(request, pk):
    challenge = get_object_or_404(EditingChallenge, pk=pk)
    if challenge.created_by != request.user:
        messages.error(request, "Du hast keine Berechtigung, diese Challenge zu löschen.")
        return redirect(reverse('editing_challenge:editing_challenge_list_private'))

    challenge.delete()
    messages.success(request, "Die Editing Challenge wurde erfolgreich gelöscht.")
    return redirect(reverse('editing_challenge:editing_challenge_list_private'))

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

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(EditingChallengeComment, id=comment_id)
    if comment.user != request.user:
        raise PermissionDenied("You are not allowed to edit this comment.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
        return redirect('editing_challenge:editing_challenge_detail', pk=comment.submission.challenge.id)
    elif request.method == 'GET' and request.is_ajax():
        return JsonResponse({'text': comment.text})

    return redirect('editing_challenge:editing_challenge_detail', pk=comment.submission.challenge.id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(EditingChallengeComment, id=comment_id)
    if comment.user != request.user:
        raise PermissionDenied("You are not allowed to delete this comment.")
    
    challenge_id = comment.submission.challenge.id
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('editing_challenge:editing_challenge_detail', pk=challenge_id)

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
        return EditingChallenge.objects.all().order_by('end_date')

@login_required
def download_file(request, pk):
    challenge = get_object_or_404(EditingChallenge, pk=pk)
    file_path = challenge.raw_file.path
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        return response
    else:
        raise Http404("File does not exist")
    
@login_required
def delete_submission(request, submission_id):
    submission = get_object_or_404(EditingChallengeSubmission, id=submission_id)

    if submission.user != request.user:
        raise PermissionDenied("You are not allowed to delete this submission.")

    # Delete all related votes and comments
    submission.votes.all().delete()
    submission.comments.all().delete()

    # Delete the submission itself
    submission.delete()

    messages.success(request, "Submission deleted successfully.")
    return redirect('editing_challenge:editing_challenge_detail', pk=submission.challenge.id)
