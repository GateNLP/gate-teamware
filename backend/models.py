import django
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class ServiceUser(AbstractUser):
    """
    Custom user class.
    """
    annotates = models.ForeignKey("Project", on_delete=models.SET_NULL, related_name="annotators", null=True)
    manages = models.ManyToManyField("Project", related_name="managers")
    created = models.DateTimeField(default=timezone.now)


class Project(models.Model):
    """
    Model to store annotation projects.
    """
    name = models.TextField(default="New project")
    description = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    configuration = models.JSONField(default=list)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="owns")
    annotations_per_doc = models.IntegerField(default=3)
    annotator_max_annotation = models.FloatField(default=0.6)
    annotation_timeout = models.IntegerField(default=60)

    @property
    def num_annotation_tasks_total(self):
        return self.documents.count() * self.annotations_per_doc

    @property
    def num_completed_tasks(self):
        num_tasks = 0
        for doc in self.documents.all():
            num_tasks += doc.annotations.filter(completed__isnull=False).count()

        return num_tasks

    @property
    def num_occupied_tasks(self):
        num_tasks = 0
        for doc in self.documents.all():
            num_tasks += doc.annotations.filter(rejected=None)

        return num_tasks

    @property
    def num_annotation_tasks_remaining(self):
        return self.num_annotation_tasks_total - self.num_occupied_tasks

    def user_reached_quota(self, user):
        num_docs = self.documents.count()
        num_user_annotated_docs = user.annotations.filter(document__in=self.documents, rejected=None).count()
        percentage_of_docs_annotated = num_user_annotated_docs / num_docs
        return percentage_of_docs_annotated >= self.annotator_max_annotation

    def get_current_annotator_task(self, user):

        current_annotations = user.annotations.filter(completed=None, rejected=None)
        num_annotations = current_annotations.count()
        if num_annotations > 1:
            raise RuntimeError("Working on more than one annotation at a time! Should not be possible!")

        if num_annotations <= 0:
            return None

        annotation = current_annotations.first()
        if annotation.document.project != self:
            return RuntimeError(
                "The annotation doesn't belong to this project! Annotator should only work on one project at a time")

        return annotation

    def assign_annotator_task(self, user):
        if self.num_annotation_tasks_remaining > 0 and not self.user_reached_quota(user):
            for doc in self.documents.all():
                # Check that annotator hasn't annotated
                if doc.user_can_annotate_document(user):
                    # Returns a new annotation (task) if so
                    return Annotation.objects.create(user=user, document=self)

        return None

    def remove_annotator_from_project(self, user):
        user.annotates = None
        user.save()
        return True

class Document(models.Model):
    """
    Model to represent a document.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    data = models.JSONField(default=dict)
    created = models.DateTimeField(default=timezone.now)

    def user_can_annotate_document(self, user):
        num_user_annotation_in_doc = self.annotations.filter(user=user).count()
        if num_user_annotation_in_doc > 1:
            raise RuntimeError(
                f"The user {user.username} has more than one annotation ({num_user_annotation_in_doc}) in the document.")

        return num_user_annotation_in_doc < 1



class Annotation(models.Model):
    """
    Model to represent a single annotation.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="annotations", null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="annotations")
    data = models.JSONField(default=dict)
    created = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(default=None, null=True)
    rejected = models.DateTimeField(default=None, null=True)
