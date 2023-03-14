import sys, os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = "If no superusers in database, create one from credentials supplied in environment variables"

    def handle(self, *args, **options):
        User = get_user_model()
        su_count = User.objects.filter(is_superuser=True).count()
        if su_count == 0:
            username = os.environ.get("SUPERUSER_USERNAME")
            password = os.environ.get("SUPERUSER_PASSWORD")
            email = os.environ.get("SUPERUSER_EMAIL")

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, password=password, email=email,
                                              is_account_activated=True)

                self.stdout.write(f'No superusers found in database.\nSuperuser created with username {username}')
            else:
                self.stdout.write(self.style.ERROR('Username already exists'))
                raise CommandError("Username already exists")

        else:
            self.stdout.write(f'{su_count} Superusers found in database.')




