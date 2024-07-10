from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if none exists, otherwise raises an error'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            raise CommandError('A superuser already exists. Use the admin interface to create additional users.')
        
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = input('Enter password: ')
        
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))