from django.shortcuts import render
from members.models import CustomUser
from meetups.models import Meetup
from django.utils import timezone

def index(request):
    newest_users = CustomUser.objects.order_by('-date_joined')[:3]
    upcoming_meetup = Meetup.objects.filter(date__gte=timezone.now()).order_by('date').first()
    return render(request, 'main/index.html', {'newest_users': newest_users, 'upcoming_meetup': upcoming_meetup})
