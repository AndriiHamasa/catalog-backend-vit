from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create superuser if not exists'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if not password:
            self.stdout.write(self.style.ERROR('DJANGO_SUPERUSER_PASSWORD not set!'))
            return
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser {username} created!'))
        else:
            self.stdout.write(self.style.WARNING(f'ℹ️ Superuser {username} already exists'))
