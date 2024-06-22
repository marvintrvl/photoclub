from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def profile_detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'members/profile_detail.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('members:profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'members/profile_edit.html', {'form': form})

def member_list(request):
    profiles = Profile.objects.all()
    return render(request, 'members/member_list.html', {'profiles': profiles})
