from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Meetup, MeetupImage
from .forms import MeetupForm

def meetup_list(request):
    meetups = Meetup.objects.all().order_by('date')
    return render(request, 'meetups/meetup_list.html', {'meetups': meetups})

def meetup_detail(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    images = MeetupImage.objects.filter(meetup=meetup)
    form = MeetupForm(instance=meetup)
    return render(request, 'meetups/meetup_detail.html', {'meetup': meetup, 'images': images, 'form': form})

@login_required
def meetup_list_private(request):
    meetups = Meetup.objects.all().order_by('date')
    return render(request, 'meetups/meetup_list_private.html', {'meetups': meetups})

@login_required
def meetup_edit(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    if request.method == 'POST':
        form = MeetupForm(request.POST, instance=meetup)
        if form.is_valid():
            form.save()
            return redirect('meetup_list_private')
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
