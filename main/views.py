from django.shortcuts import render
from members.models import CustomUser

# Create your views here.
def index(request):
    newest_users = CustomUser.objects.order_by('-date_joined')[:3]
    return render(request, 'main/index.html', {'newest_users': newest_users})
