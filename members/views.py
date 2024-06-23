from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import ProfileForm, LoginForm
from django.contrib.auth import authenticate, login, logout

@login_required
def profile_edit(request):
    user = request.user  # Get the authenticated user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('members:profile_edit')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'members/profile_edit.html', {'form': form, 'user': user})

def member_list(request):
    profiles = CustomUser.objects.all()
    return render(request, 'members/member_list.html', {'profiles': profiles})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Ungültiger Benutzername oder Passwort')
    else:
        form = LoginForm()
    return render(request, 'members/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def member_detail(request, username):
    member = get_object_or_404(CustomUser, username=username)
    return render(request, 'members/member_detail.html', {'member': member})