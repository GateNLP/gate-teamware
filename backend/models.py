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


class Project(models.Model):
    """
    Model to store annotation projects.
    """
    name = models.TextField(default="New project")
    created_at = models.DateTimeField(default=timezone.now)
    data = models.JSONField(default=dict)
    configuration = models.JSONField(default=dict)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="owns")

    def export_annotations(self):
        pass

    def add_annotator(self, user):
        pass

    def remove_annotator(self, user):
        pass

    def add_manager(self, user):
        pass

    def remove_manager(self, user):
        pass

    def set_owner(self, user):
        pass

    def transfer_owner(self, old_owner, new_owner):
        pass



class Document(models.Model):
    """
    Model to represent a document.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)


class Annotation(models.Model):
    """
    Model to represent a single annotation.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="annotations", null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="annotations")
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)

