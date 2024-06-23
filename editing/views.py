# editing/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import EditingChallenge, EditingSubmission
from django.contrib.auth.decorators import login_required
from .forms import EditingSubmissionForm

def editing_list(request):
    challenges = EditingChallenge.objects.all()
    return render(request, 'editing/editing_list.html', {'challenges': challenges})

def editing_detail(request, challenge_id):
    challenge = get_object_or_404(EditingChallenge, pk=challenge_id)
    submissions = challenge.submissions.all()
    return render(request, 'editing/editing_detail.html', {'challenge': challenge, 'submissions': submissions})

@login_required
def editing_edit(request):
    if request.method == 'POST':
        form = EditingSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return redirect('editing_detail', challenge_id=submission.challenge.id)
    else:
        form = EditingSubmissionForm()
    return render(request, 'editing/editing_edit.html', {'form': form})
