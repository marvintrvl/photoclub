from django.shortcuts import render
from members.models import CustomUser
from meetups.models import Meetup
from photo_challenge.models import PhotoChallenge
from editing_challenge.models import EditingChallenge
from .models import HomePageImage
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import logging

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

def impressum(request):
    return render(request, 'main/impressum.html')

logger = logging.getLogger(__name__)

def kontakt(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Customize the email content
        subject = f'Neue Kontaktanfrage von {fullname}'
        message_body = f'Name: {fullname}\nE-Mail: {email}\nNachricht:\n{message}'
        
        try:
            send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
            messages.success(request, 'Ihre Nachricht wurde erfolgreich gesendet!')
        except Exception as e:
            messages.error(request, f'Es gab einen Fehler beim Senden der Nachricht: {e}')
        
        return redirect('kontakt')
    
    return render(request, 'main/kontakt.html')


def datenschutzerklaerung(request):
    return render(request, 'main/datenschutzerklaerung.html')
