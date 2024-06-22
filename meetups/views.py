from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Meetup
from .forms import MeetupForm

def meetup_list(request):
    meetups = Meetup.objects.all()
    return render(request, 'meetups/meetup_list.html', {'meetups': meetups})

def meetup_detail(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    return render(request, 'meetups/meetup_detail.html', {'meetup': meetup})

@login_required
def meetup_edit(request, pk=None):
    if pk:
        meetup = get_object_or_404(Meetup, pk=pk)
    else:
        meetup = Meetup()
    
    if request.method == 'POST':
        form = MeetupForm(request.POST, instance=meetup)
        if form.is_valid():
            form.save()
            return redirect('meetups:meetup_list')
    else:
        form = MeetupForm(instance=meetup)
    
    return render(request, 'meetups/meetup_edit.html', {'form': form})
