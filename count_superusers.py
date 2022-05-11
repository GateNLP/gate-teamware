import sys
import django
from django.contrib.auth import get_user_model

django.setup()
User = get_user_model()
sys.stdout.write(str(User.objects.filter(is_superuser=True).count()))
