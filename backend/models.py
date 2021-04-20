import django
from django.contrib.auth.models import AbstractUser
from django.db import models


class ServiceUser(AbstractUser):
    """
    Custom user class.
    """
    annotates = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="annotators")
    

class Project(models.Model):
    """
    Model to store annotation projects.
    """
    name = models.TextField()
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    managers = models.ManyToManyField(ServiceUser, related_name="manages")
    owner = models.OneToOneField(ServiceUser, related_name="owns")
    data = models.JSONField()

    def export_annotations():
        pass

    def add_annotator(user):
        pass

    def remove_annotator(user):
        pass

    def add_manager(user):
        pass

    def remove_manager(user):
        pass

    def set_owner(user):
        pass

    def transfer_owner(old_owner,new_owner):
        pass


class Document(models.Model):
    """
    Model to represent a document.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    data = models.JSONField()


class Annotation(models.Model):
    """
    Model to represent a single annotation.
    """
    user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name="annotations")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="annotations")
    data = models.JSONField()
