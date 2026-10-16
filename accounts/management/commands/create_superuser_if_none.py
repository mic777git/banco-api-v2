import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write('Variaveis DJANGO_SUPERUSER_USERNAME ou DJANGO_SUPERUSER_PASSWORD nao definidas, pulando.')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Usuario {username} ja existe, pulando.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(f'Superusuario {username} criado com sucesso.')