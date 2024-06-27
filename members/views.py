from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, PhotoCategory, UserPhoto, Equipment, Interest, PhotoGenre, Steckbrief
from .forms import ProfileForm, LoginForm, PhotoCategoryForm, UserPhotoForm, EquipmentForm, InterestForm, PhotoGenreForm, SteckbriefForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist

@login_required
def profile_edit(request):
    user = request.user
    try:
        steckbrief = user.steckbrief
    except ObjectDoesNotExist:
        steckbrief = Steckbrief.objects.create(user=user, image_editing=False, preferred_shooting='alone')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        equipment_form = EquipmentForm(request.POST, prefix='equipment')
        interest_form = InterestForm(request.POST, prefix='interest')
        photo_genre_form = PhotoGenreForm(request.POST, prefix='photo_genre')
        steckbrief_form = SteckbriefForm(request.POST, instance=steckbrief)

        if all([form.is_valid(), equipment_form.is_valid(), interest_form.is_valid(), 
                photo_genre_form.is_valid(), steckbrief_form.is_valid()]):
            form.save()
            if equipment_form.has_changed():
                equipment = equipment_form.save(commit=False)
                equipment.user = user
                equipment.save()
            if interest_form.has_changed():
                interest = interest_form.save(commit=False)
                interest.user = user
                interest.save()
            if photo_genre_form.has_changed():
                photo_genre = photo_genre_form.save(commit=False)
                photo_genre.user = user
                photo_genre.save()
            steckbrief_form.save()
            return redirect('members:profile_edit')
    else:
        form = ProfileForm(instance=user)
        equipment_form = EquipmentForm(prefix='equipment')
        interest_form = InterestForm(prefix='interest')
        photo_genre_form = PhotoGenreForm(prefix='photo_genre')
        steckbrief_form = SteckbriefForm(instance=steckbrief)

    context = {
        'form': form,
        'equipment_form': equipment_form,
        'interest_form': interest_form,
        'photo_genre_form': photo_genre_form,
        'steckbrief_form': steckbrief_form,
        'user': user,
    }
    return render(request, 'members/profile_edit.html', context)

@login_required
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk, user=request.user)
    equipment.delete()
    return redirect('members:profile_edit')

@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.user = request.user
            equipment.save()
    return redirect('members:profile_edit')

@login_required
def delete_interest(request, pk):
    interest = get_object_or_404(Interest, pk=pk, user=request.user)
    interest.delete()
    return redirect('members:profile_edit')

@login_required
def add_interest(request):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.user = request.user
            interest.save()
    return redirect('members:profile_edit')

@login_required
def delete_photo_genre(request, pk):
    photo_genre = get_object_or_404(PhotoGenre, pk=pk, user=request.user)
    photo_genre.delete()
    return redirect('members:profile_edit')

@login_required
def add_photo_genre(request):
    if request.method == 'POST':
        form = PhotoGenreForm(request.POST)
        if form.is_valid():
            photo_genre = form.save(commit=False)
            photo_genre.user = request.user
            photo_genre.save()
    return redirect('members:profile_edit')

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

@login_required
def add_category(request):
    if request.method == 'POST':
        form = PhotoCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('members:profile_edit')
    else:
        form = PhotoCategoryForm()
    return render(request, 'members/profile_edit.html', {'form': form})

@login_required
def add_photo(request):
    if request.method == 'POST':
        form = UserPhotoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            
            # Check if the category belongs to the current user
            if photo.category.user != request.user:
                return HttpResponseForbidden("You can't add photos to categories that don't belong to you.")
            
            photo.save()
            return redirect('members:profile_edit')
    else:
        form = UserPhotoForm(user=request.user)
    
    # Limit category choices to the current user's categories
    form.fields['category'].queryset = PhotoCategory.objects.filter(user=request.user)
    
    return render(request, 'members/profile_edit.html', {'form': form})

@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(UserPhoto, pk=pk, user=request.user)
    photo.delete()
    return redirect('members:profile_edit')
