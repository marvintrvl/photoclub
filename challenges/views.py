from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Challenge
from .forms import ChallengeForm

def challenge_list(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/challenge_list.html', {'challenges': challenges})

def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})

@login_required
def challenge_edit(request, pk=None):
    if pk:
        challenge = get_object_or_404(Challenge, pk=pk)
    else:
        challenge = Challenge()
    
    if request.method == 'POST':
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
            return redirect('challenges:challenge_list')
    else:
        form = ChallengeForm(instance=challenge)
    
    return render(request, 'challenges/challenge_edit.html', {'form': form})
