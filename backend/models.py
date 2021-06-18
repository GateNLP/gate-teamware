import logging
import django
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.db.models import Q, F

log = logging.getLogger(__name__)


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
            num_tasks += doc.num_completed_annotations

        return num_tasks

    @property
    def num_occupied_tasks(self):
        num_tasks = 0
        for doc in self.documents.all():
            num_tasks += doc.num_completed_and_pending_annotations

        return num_tasks

    @property
    def num_annotation_tasks_remaining(self):
        return self.num_annotation_tasks_total - self.num_occupied_tasks

    @property
    def is_completed(self):
        # Project must have documents to be completed
        if self.num_annotation_tasks_total <= 0:
            return False

        return self.num_annotation_tasks_total - self.num_completed_tasks < 1

    def add_annotator(self, user):
        self.annotators.add(user)
        self.save()

    def remove_annotator(self, user):
        self.annotators.remove(user)
        self.save()

    def annotator_reached_quota(self, user):
        num_docs = self.documents.count()
        num_user_annotated_docs = 0
        for doc in self.documents.all():
            if doc.user_completed_annotation_of_document(user):
                num_user_annotated_docs += 1

        percentage_of_docs_annotated = num_user_annotated_docs / num_docs
        return percentage_of_docs_annotated >= self.annotator_max_annotation

    def get_current_annotator_task(self, user):

        current_annotations = user.annotations.filter(completed=None, rejected=None, timed_out=None)
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
        if self.num_annotation_tasks_remaining > 0:
            for doc in self.documents.all():
                # Check that annotator hasn't annotated and that
                # doc hasn't been fully annotated
                if doc.user_can_annotate_document(user):
                    # Returns a new annotation (task) if so
                    return Annotation.objects.create(user=user,
                                                     document=doc,
                                                     times_out_at=timezone.now() + timedelta(
                                                         minutes=self.annotation_timeout))

        return None

    def check_project_complete(self):
        """ Checks that all annotations have been completed, release all annotators from project. """
        if self.is_completed:
            for annotator in self.annotators.all():
                self.remove_annotator(annotator)



class Document(models.Model):
    """
    Model to represent a document.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    data = models.JSONField(default=dict)
    created = models.DateTimeField(default=timezone.now)

    @property
    def num_completed_annotations(self):
        return self.annotations.filter(completed__isnull=False).count()

    @property
    def num_rejected_annotations(self):
        return self.annotations.filter(rejected__isnull=False).count()

    @property
    def num_timed_out_annotations(self):
        return self.annotations.filter(timed_out__isnull=False).count()

    @property
    def num_pending_annotations(self):
        return self.annotations.filter(completed=None, rejected=None, timed_out=None).count()

    @property
    def num_completed_and_pending_annotations(self):
        return self.annotations.filter(
            Q(completed__isnull=False) | Q(completed=None, rejected=None, timed_out=None)).count()

    def user_can_annotate_document(self, user):
        num_user_annotation_in_doc = self.num_completed_and_pending_user_annotations(user)
        if num_user_annotation_in_doc > 1:
            raise RuntimeError(
                f"The user {user.username} has more than one annotation ({num_user_annotation_in_doc}) in the document.")

        return num_user_annotation_in_doc < 1

    def num_completed_and_pending_user_annotations(self, user):
        return self.annotations.filter(
            Q(user=user, completed__isnull=False) |
            Q(user=user, completed=None, rejected=None, timed_out=None)).count()

    def user_completed_annotation_of_document(self, user):
        for annotation in self.annotations.all():
            if annotation.user == user:
                if annotation.completed:
                    return True

        return False


class Annotation(models.Model):
    """
    Model to represent a single annotation.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="annotations", null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="annotations")
    data = models.JSONField(default=dict)
    times_out_at = models.DateTimeField(default=None, null=True)
    created = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(default=None, null=True)
    rejected = models.DateTimeField(default=None, null=True)
    timed_out = models.DateTimeField(default=None, null=True)

    def get_annotation_task(self):
        document = self.document
        project = self.document.project
        return {
            "project_name": project.name,
            "project_description": project.description,
            "project_config": project.configuration,
            "project_id": project.pk,
            "document_id": document.pk,
            "document_data": document.data,
            "annotation_id": self.pk,
            "annotation_timeout": self.times_out_at
        }

    def complete_annotation(self, data, completed_time=timezone.now()):
        self.check_not_completed_rejected_or_timed_out()
        self.data = data
        self.completed = completed_time
        self.save()

        # Also check whether the project has been completed
        self.document.project.check_project_complete()

    def reject_annotation(self, rejected_time=timezone.now()):
        self.check_not_completed_rejected_or_timed_out()
        self.rejected = rejected_time
        self.save()

    def timeout_annotation(self, timeout_time=timezone.now()):
        self.check_not_completed_rejected_or_timed_out()
        self.timed_out = timeout_time
        self.save()

    def check_not_completed_rejected_or_timed_out(self):
        if self.completed:
            log.warning(f"Annotation id {self.id} is already completed.")
            raise RuntimeError("The annotation is already completed.")

        if self.rejected:
            log.warning(f"Annotation id {self.id} is already rejected.")
            raise RuntimeError("The annotation is already rejected.")

        if self.timed_out:
            log.warning(f"Annotation id {self.id} is already timed out.")
            raise RuntimeError("The annotation is already timed out.")

    def user_allowed_to_annotate(self, user):
        return self.user.id == user.id


    @staticmethod
    def check_for_timed_out_annotations(current_time=timezone.now()):
        """
        Checks for any annotation that has timed out (times_out_at < current_time) and set the timed_out property
        to the current_time.

        Returns the of annotations that has become timed out.
        """
        timed_out_annotations = Annotation.objects.filter(times_out_at__lt=current_time,
                                                          timed_out__isnull=True,
                                                          completed__isnull=True,
                                                          rejected__isnull=True)
        for annotation in timed_out_annotations:
            annotation.timeout_annotation(current_time)

        return len(timed_out_annotations)

