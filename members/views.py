from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import CustomUser, PhotoCategory, UserPhoto, Equipment, Interest, PhotoGenre, Steckbrief
from .forms import ProfileForm, LoginForm, PhotoCategoryForm, UserPhotoForm, EquipmentForm, InterestForm, PhotoGenreForm, SteckbriefForm
from django.contrib.auth import authenticate, login, logout

@login_required
def profile_edit(request):
    user = request.user
    form = ProfileForm(instance=user)
    equipment_form = EquipmentForm()
    interest_form = InterestForm()
    photo_genre_form = PhotoGenreForm()

    # Ensure Steckbrief instance exists
    steckbrief, created = Steckbrief.objects.get_or_create(user=user, defaults={'image_editing': False, 'preferred_shooting': 'alone'})

    steckbrief_form = SteckbriefForm(instance=steckbrief)
    categories = PhotoCategory.objects.filter(user=request.user)
    category_form = PhotoCategoryForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('members:profile_edit')
    
    context = {
        'form': form,
        'equipment_form': equipment_form,
        'interest_form': interest_form,
        'photo_genre_form': photo_genre_form,
        'steckbrief_form': steckbrief_form,
        'categories': categories,
        'category_form': category_form,
    }
    return render(request, 'members/profile_edit.html', context)

@login_required
@require_POST
def add_equipment(request):
    form = EquipmentForm(request.POST)
    if form.is_valid():
        equipment = form.save(commit=False)
        equipment.user = request.user
        equipment.save()
        return JsonResponse({
            'success': True,
            'id': equipment.id,
            'category': equipment.get_category_display(),
            'name': equipment.name
        })
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def delete_equipment(request, pk):
    try:
        equipment = Equipment.objects.get(pk=pk, user=request.user)
        equipment.delete()
        return JsonResponse({'success': True})
    except Equipment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Equipment not found'})

@login_required
@require_POST
def add_interest(request):
    form = InterestForm(request.POST)
    if form.is_valid():
        interest = form.save(commit=False)
        interest.user = request.user
        interest.save()
        return JsonResponse({
            'success': True,
            'id': interest.id,
            'name': interest.name
        })
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def delete_interest(request, pk):
    try:
        interest = Interest.objects.get(pk=pk, user=request.user)
        interest.delete()
        return JsonResponse({'success': True})
    except Interest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Interest not found'})

@login_required
@require_POST
def add_photo_genre(request):
    form = PhotoGenreForm(request.POST)
    if form.is_valid():
        photo_genre = form.save(commit=False)
        photo_genre.user = request.user
        photo_genre.save()
        return JsonResponse({
            'success': True,
            'id': photo_genre.id,
            'name': photo_genre.name
        })
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def delete_photo_genre(request, pk):
    try:
        photo_genre = PhotoGenre.objects.get(pk=pk, user=request.user)
        photo_genre.delete()
        return JsonResponse({'success': True})
    except PhotoGenre.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Photo genre not found'})

@login_required
@require_POST
def manage_steckbrief(request):
    user = request.user
    steckbrief, created = Steckbrief.objects.get_or_create(user=user)
    form = SteckbriefForm(request.POST, instance=steckbrief)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

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
    equipment = member.equipment.all()
    interests = member.interests.all()
    photo_genres = member.photo_genres.all()
    steckbrief = getattr(member, 'steckbrief', None)  # Safely get steckbrief or None if it doesn't exist
    
    # Group equipment by category
    grouped_equipment = {}
    for item in equipment:
        if item.category not in grouped_equipment:
            grouped_equipment[item.category] = []
        grouped_equipment[item.category].append(item.name)
    
    context = {
        'member': member,
        'grouped_equipment': grouped_equipment,
        'interests': interests,
        'photo_genres': photo_genres,
        'steckbrief': steckbrief,  # Pass None if steckbrief doesn't exist
    }
    return render(request, 'members/member_detail.html', context)

@login_required
def manage_categories(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            form = PhotoCategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()
        elif action == 'update':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(PhotoCategory, id=category_id, user=request.user)
            form = PhotoCategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
        elif action == 'delete':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(PhotoCategory, id=category_id, user=request.user)
            category.delete()
        
        return redirect('members:profile_edit')
    
    # If it's a GET request, we'll handle this in the profile_edit view
    return redirect('members:profile_edit')

@login_required
def add_photo(request):
    if request.method == 'POST':
        form = UserPhotoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            
            if photo.category.user != request.user:
                return HttpResponseForbidden("You can't add photos to categories that don't belong to you.")
            
            photo.save()
            return redirect('members:profile_edit')
    else:
        form = UserPhotoForm(user=request.user)
    
    form.fields['category'].queryset = PhotoCategory.objects.filter(user=request.user)
    
    return render(request, 'members/profile_edit.html', {'form': form})

@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(UserPhoto, pk=pk, user=request.user)
    photo.delete()
    return redirect('members:profile_edit')