import sys, os
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from backend.models import Project, Document, Annotation
from backend.rpc import _generate_user_activation
from django.core.management import call_command

TEST_FIXTURES_REGISTRY = {}


def test_fixture(func):
    TEST_FIXTURES_REGISTRY[func.__name__] = func
    return func


@test_fixture
def create_db_users():
    """Create default db users, admin, manager and annotator with password: testpassword"""
    password = "testpassword"
    admin = get_user_model().objects.create_user(username="admin", password=password)
    admin.is_superuser = True
    admin.is_staff = True
    admin.is_account_activated = True
    admin.save()

    manager = get_user_model().objects.create_user(username="manager", password=password)
    manager.is_manager = True
    manager.is_account_activated = True
    manager.save()

    annotator = get_user_model().objects.create_user(username="annotator", password=password)
    annotator.is_account_activated = True
    annotator.save()


@test_fixture
def create_db_users_with_project_and_annotation():
    """Create default db users and also create a set of annotation."""
    create_db_users()
    admin_user = get_user_model().objects.get(username="admin")

    project_config = [
        {
            "name": "htmldisplay",
            "type": "html",
            "text": "{{{text}}}"
        },
        {
            "name": "sentiment",
            "type": "radio",
            "title": "Sentiment",
            "description": "Please select a sentiment of the text above.",
            "options": {
                "negative": "Negative",
                "neutral": "Neutral",
                "positive": "Positive"
            }
        }
    ]

    project = Project.objects.create(name="Test project", owner=admin_user, configuration=project_config)
    for i in range(20):
        doc_data = {
            "text": f"Document text {i}"
        }
        document = Document.objects.create(project=project, data=doc_data)
        annotation = Annotation.objects.create(document=document, user=admin_user,
                                               status=Annotation.COMPLETED, status_time=timezone.now())
        annotation.data = {"sentiment": "positive"}


class Command(BaseCommand):

    help = "Flushes the database and loads a test fixture"

    def add_arguments(self, parser):
        parser.add_argument("-n", "--name", type=str, help="Name of the fixture")

    def handle(self, *args, **options):
        # Flush the DB
        if "name" in options and options["name"] and options["name"] in TEST_FIXTURES_REGISTRY:
            # Flush the DB
            call_command("flush", "--noinput")
            # Run the fixture function
            TEST_FIXTURES_REGISTRY[options["name"]]()

        else:
            # List available fixtures
            print("No fixture specified, used the -n, --name option. Available fixtures are:")
            for name, func in TEST_FIXTURES_REGISTRY.items():
                func_help_str = f"- {func.__doc__}" if func.__doc__ else ""
                print(f"{name} {func_help_str}")
