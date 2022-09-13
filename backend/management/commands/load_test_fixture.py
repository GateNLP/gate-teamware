from multiprocessing.connection import wait
import sys, os
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from backend.models import AnnotatorProject, Project, Document, Annotation, DocumentType
from django.core.management import call_command

TEST_FIXTURES_REGISTRY = {}


def test_fixture(func):
    TEST_FIXTURES_REGISTRY[func.__name__] = func
    return func


@test_fixture
def create_db_users():
    """Create default db users, admin, manager and annotator with password: testpassword"""
    password = "testpassword"
    admin = get_user_model().objects.create_user(username="admin", password=password, email="admin@test.com")
    admin.is_superuser = True
    admin.is_staff = True
    admin.is_account_activated = True
    admin.save()

    manager = get_user_model().objects.create_user(username="manager", password=password, email="manager@test.com")
    manager.is_manager = True
    manager.is_account_activated = True
    manager.save()

    annotator = get_user_model().objects.create_user(username="annotator", password=password, email="annotator@test.com")
    annotator.is_account_activated = True
    annotator.save()


@test_fixture
def create_db_users_with_project_and_annotation():
    """Create default db users and also create a set of annotation."""
    create_db_users()
    admin_user = get_user_model().objects.get(username="admin")
    manager_user = get_user_model().objects.get(username="manager")
    annotator_user = get_user_model().objects.get(username="annotator")
    users = [admin_user, manager_user, annotator_user]

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

    project = Project.objects.create(name="Test project",
                                     owner=admin_user,
                                     configuration=project_config,
                                     has_test_stage=False,
                                     has_training_stage=False,
                                     allow_annotation_change=True,
                                     document_id_field="id")
    for i in range(20):
        doc_data = {
            "id": f"{i+1}",
            "text": f"Document text {i}"
        }
        document = Document.objects.create(project=project, data=doc_data)
        for user in users:
            annotation = Annotation.objects.create(document=document, user=user,
                                               status=Annotation.COMPLETED, status_time=timezone.now())
            annotation.data = {"sentiment": "positive"}


@test_fixture
def project_with_training_and_test():
    """Creates a project with training and test phases and documents"""

    create_db_users_with_project_and_annotation()

    project = Project.objects.first()
    project.has_training_stage = True
    project.has_test_stage = True
    project.save()

    num_documents = 10

    # Create training and test documents
    for i in range(num_documents):
        doc_data = {
            "id": f"{i+1}",
            "text": f"Document text {i}",
            "gold": {
                "sentiment": {
                    "value": "positive",
                    "explanation": "Example explanation"
                }
            }
        }
        document = Document.objects.create(project=project, data=doc_data, doc_type=DocumentType.TRAINING)
        document = Document.objects.create(project=project, data=doc_data, doc_type=DocumentType.TEST)


@test_fixture
def project_with_annotators():
    """
    Fixture for testing the annotator management view.
    Create default db users, set of annotations and add annotators to project.
    Users are specified at particular stages:
    - Training
    - Testing (Pass)
    - Testing (Fail)
    - Annotating
    - Completion
    """

    project_with_training_and_test()

    annotation_user = get_user_model().objects.get(username="annotator")
    waiting_user = get_user_model().objects.create(username="waiter")
    training_user = get_user_model().objects.create(username="trainer")
    testing_user = get_user_model().objects.create(username="tester")
    failing_user = get_user_model().objects.create(username="failer")
    completed_user = get_user_model().objects.create(username="completer")

    project = Project.objects.first()

    for annotator in [annotation_user, waiting_user, training_user, testing_user, failing_user, completed_user]:
        project.add_annotator(annotator)
    project.save()

    # Users that complete training
    for user in [annotation_user, waiting_user, completed_user, testing_user, failing_user]:
        for document in project.documents.filter(doc_type=DocumentType.TRAINING):
            annotation = Annotation.objects.create(document=document, user=user,
                                                status=Annotation.COMPLETED, status_time=timezone.now())
            annotation.data = {"sentiment": "positive"}
            annotation.save()
        project.annotator_completed_training(user)
        project.save()

    # Training user doesn't complete training
    for document in project.documents.filter(doc_type=DocumentType.TRAINING)[:5]:
        annotation = Annotation.objects.create(document=document, user=training_user,
                                            status=Annotation.COMPLETED, status_time=timezone.now())
        annotation.data = {"sentiment": "positive"}
        annotation.save()
    annotator_project = AnnotatorProject.objects.get(project=project, annotator=training_user)
    annotator_project.training_score = project.get_annotator_document_score(training_user, DocumentType.TRAINING)
    annotator_project.save()

    # Users that complete testing
    for user in [annotation_user, waiting_user, completed_user]:
        for document in project.documents.filter(doc_type=DocumentType.TEST):
            annotation = Annotation.objects.create(document=document, user=user,
                                                status=Annotation.COMPLETED, status_time=timezone.now())
            annotation.data = {"sentiment": "positive"}
            annotation.save()
        project.annotator_completed_test(user)
        project.save()

    # Testing user doesn't complete testing
    for document in project.documents.filter(doc_type=DocumentType.TEST)[:5]:
        annotation = Annotation.objects.create(document=document, user=testing_user,
                                            status=Annotation.COMPLETED, status_time=timezone.now())
        annotation.data = {"sentiment": "positive"}
        annotation.save()
    annotator_project = AnnotatorProject.objects.get(project=project, annotator=testing_user)
    annotator_project.test_score = project.get_annotator_document_score(testing_user, DocumentType.TEST)
    annotator_project.save()

    # Failing user fails testing
    for document in project.documents.filter(doc_type=DocumentType.TEST):
        annotation = Annotation.objects.create(document=document, user=failing_user,
                                            status=Annotation.COMPLETED, status_time=timezone.now())
        annotation.data = {"sentiment": "negative"}
        annotation.save()
    # project.get_annotator_document_score(failing_user, DocumentType.TEST)
    # project.save()
    project.annotator_completed_test(failing_user)
    project.save()

    # Completed user's annotations
    for document in project.documents.filter(doc_type=DocumentType.ANNOTATION):
        annotation = Annotation.objects.create(document=document, user=completed_user,
                                            status=Annotation.COMPLETED, status_time=timezone.now())
        annotation.data = {"sentiment": "positive"}
        annotation.save()
    ann_proj = AnnotatorProject.objects.get(project=project, annotator=completed_user)
    ann_proj.annotations_completed = timezone.now()
    ann_proj.save()
    



class Command(BaseCommand):

    help = "Flushes the database and loads a test fixture"

    def add_arguments(self, parser):
        parser.add_argument("-n", "--name", type=str, help="Name of the fixture")

    def handle(self, *args, **options):
        # Flush the DB
        if "name" in options and options["name"] and options["name"] in TEST_FIXTURES_REGISTRY:
            # Flush the DB
            print("Flushing database...")
            call_command("flush", "--noinput")
            print("Migrating database...")
            call_command("migrate", "--noinput")
            # Run the fixture function
            print(f"Running command {options['name']}")
            TEST_FIXTURES_REGISTRY[options["name"]]()


        else:
            # List available fixtures
            print("No fixture specified, used the -n, --name option. Available fixtures are:")
            for name, func in TEST_FIXTURES_REGISTRY.items():
                func_help_str = f"- {func.__doc__}" if func.__doc__ else ""
                print(f"{name} {func_help_str}")
