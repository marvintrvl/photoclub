from django.shortcuts import render
from members.models import CustomUser
from meetups.models import Meetup
from photo_challenge.models import PhotoChallenge
from editing_challenge.models import EditingChallenge
from .models import HomePageImage
from django.utils import timezone

def index(request):
    newest_users = CustomUser.objects.order_by('-date_joined')[:3]
    upcoming_meetup = Meetup.objects.filter(date__gte=timezone.now()).order_by('date').first()
    nearest_photo_challenge = PhotoChallenge.objects.filter(end_date__gte=timezone.now()).order_by('end_date').first()
    nearest_editing_challenge = EditingChallenge.objects.filter(end_date__gte=timezone.now()).order_by('end_date').first()
    image_of_the_day = HomePageImage.get_image_of_the_day()
    
    return render(request, 'main/index.html', {
        'newest_users': newest_users,
        'upcoming_meetup': upcoming_meetup,
        'nearest_photo_challenge': nearest_photo_challenge,
        'nearest_editing_challenge': nearest_editing_challenge,
        'image_of_the_day': image_of_the_day,
    })
