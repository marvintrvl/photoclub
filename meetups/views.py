from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Meetup, MeetupImage
from .forms import MeetupForm, MeetupImageForm
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse

def meetup_list(request):
    today = timezone.now().date()
    upcoming_meetups = Meetup.objects.filter(date__gte=today).order_by('date')
    past_meetups = Meetup.objects.filter(date__lt=today).order_by('-date')
    return render(request, 'meetups/meetup_list.html', {
        'upcoming_meetups': upcoming_meetups,
        'past_meetups': past_meetups
    })

def meetup_detail(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = MeetupImageForm(request.POST, request.FILES)
            if form.is_valid():
                meetup_image = form.save(commit=False)
                meetup_image.meetup = meetup
                meetup_image.user = request.user
                meetup_image.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'image_url': meetup_image.image.url})
                return redirect('meetup_detail', pk=meetup.id)
        else:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
    else:
        form = MeetupImageForm()
    
    user_picture = request.user.picture.url if request.user.is_authenticated and hasattr(request.user, 'picture') else None
    username = request.user.username if request.user.is_authenticated else "Guest"
    
    return render(request, 'meetups/meetup_detail.html', {
        'meetup': meetup,
        'form': form,
        'user_picture': user_picture,
        'username': username,
    })

@login_required
def add_meetup_image(request, meetup_id):
    meetup = get_object_or_404(Meetup, id=meetup_id)
    if request.method == 'POST':
        form = MeetupImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.meetup = meetup
            image.user = request.user
            image.save()
            return JsonResponse({'success': True, 'image_url': image.image.url})
    return JsonResponse({'success': False})

@login_required
def delete_meetup_image(request, meetup_id, image_id):
    meetup = get_object_or_404(Meetup, id=meetup_id)
    image = get_object_or_404(MeetupImage, id=image_id)
    if image.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        image.delete()
        return redirect('meetup_detail', pk=meetup.id)
    return render(request, 'meetups/meetup_detail.html', {'meetup': meetup})

@login_required
def meetup_list_private(request):
    meetups = Meetup.objects.all().order_by('date')
    return render(request, 'meetups/meetup_list_private.html', {'meetups': meetups})

@login_required
def meetup_edit(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    if request.method == 'POST':
        form_data = request.POST.copy()
        if not form_data.get('date'):
            form_data['date'] = meetup.date
        if not form_data.get('time'):
            form_data['time'] = meetup.time

        form = MeetupForm(form_data, instance=meetup)
        if form.is_valid():
            form.save()
            return redirect('meetup_list_private')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = MeetupForm(instance=meetup)
    return render(request, 'meetups/meetup_edit.html', {'form': form, 'meetup': meetup})

@login_required
def meetup_create(request):
    if request.method == 'POST':
        form = MeetupForm(request.POST)
        if form.is_valid():
            meetup = form.save()
            return redirect('meetup_list_private')
    else:
        form = MeetupForm()
    return render(request, 'meetups/meetup_create.html', {'form': form})

@login_required
def delete_meetup(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)

    meetup.delete()
    messages.success(request, "Das Treffen wurde erfolgreich gelöscht.")
    return redirect(reverse('meetup_list_private'))

@login_required
def join_meetup(request, meetup_id):
    meetup = get_object_or_404(Meetup, id=meetup_id)
    meetup.attendees.add(request.user)
    return redirect('meetup_detail', pk=meetup.id)

@login_required
def leave_meetup(request, meetup_id):
    meetup = get_object_or_404(Meetup, id=meetup_id)
    meetup.attendees.remove(request.user)
    return redirect('meetup_detail', pk=meetup.id)
