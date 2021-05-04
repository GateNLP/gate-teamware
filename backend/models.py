import django
from django.contrib.auth.models import AbstractUser
from django.db import models


class ServiceUser(AbstractUser):
    """
    Custom user class.
    """
    annotates = models.ForeignKey("Project", on_delete=models.SET_NULL, related_name="annotators", null=True)
    manages = models.ManyToManyField("Project", related_name="managers")
    owns = models.ForeignKey("Project", on_delete=models.SET_NULL, related_name="owner", null=True)


class Project(models.Model):
    """
    Model to store annotation projects.
    """
    name = models.TextField()
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    data = models.JSONField()

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
    data = models.JSONField()


class Annotation(models.Model):
    """
    Model to represent a single annotation.
    """
    user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name="annotations")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="annotations")
    data = models.JSONField()
