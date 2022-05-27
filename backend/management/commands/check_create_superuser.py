import sys, os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from backend.rpc import _generate_user_activation

class Command(BaseCommand):

    help = "If no superusers in database, create one from credentials supplied in environment variables"

    def handle(self, *args, **options):
        User = get_user_model()
        su_count = User.objects.filter(is_superuser=True).count()
        if su_count == 0:
            username = os.environ.get("SUPERUSER_USERNAME")
            password = os.environ.get("SUPERUSER_PASSWORD")
            email = os.environ.get("SUPERUSER_EMAIL")

            if not get_user_model().objects.filter(username=username).exists():
                user = get_user_model().objects.create_user(username=username, password=password, email=email)
                _generate_user_activation(user)

                self.stdout.write(f'No superusers found in database.\nSuperuser created with username {username}')
            else:
                self.stdout.write(self.style.ERROR('Username already exists'))
                raise CommandError("Username already exists")

        else:
            self.stdout.write(f'{su_count} Superusers found in database.')




