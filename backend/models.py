from django.conf import settings
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
    annotates = models.ForeignKey("Project", on_delete=models.SET_NULL, related_name="annotators", null=True, blank=True)
    is_manager = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    is_account_activated = models.BooleanField(default=False)
    activate_account_token = models.TextField(null=True, blank=True)
    activate_account_token_expire = models.DateTimeField(null=True, blank=True)
    reset_password_token = models.TextField(null=True, blank=True)
    reset_password_token_expire = models.DateTimeField(null=True, blank=True)
    receive_mail_notifications = models.BooleanField(default=True)

    @property
    def is_activated(self):
        """
        Checks whether the user has activated their account, but also takes into account
        of the REGISTER_WITH_EMAIL_ACTIVATION settings.
        """
        if settings.ACTIVATION_WITH_EMAIL:
            return self.is_account_activated
        else:
            return True

    @is_activated.setter
    def is_activated(self, value):
        self.is_account_activated = value


    def is_associated_with_document(self, document):

        if self.is_manager or self.is_staff or self.is_superuser:
            return True

        return self.annotations.filter(document_id=document.pk).count() > 0 or \
               (self.annotates and self.annotates.documents.filter(pk=document.pk).count() > 0)


    def is_associated_with_annotation(self, annotation):

        if self.is_manager or self.is_staff or self.is_superuser:
            return True

        return self.annotations.filter(pk=annotation.pk).count() > 0


def default_document_input_preview():
    return {"text": "<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>"}

class Project(models.Model):
    """
    Model to store annotation projects.
    """
    name = models.TextField(default="New project")
    description = models.TextField(default="")
    annotator_guideline = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    configuration = models.JSONField(default=list)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="owns")
    annotations_per_doc = models.IntegerField(default=3)
    annotator_max_annotation = models.FloatField(default=0.6)
    annotation_timeout = models.IntegerField(default=60)
    document_input_preview = models.JSONField(default=default_document_input_preview)

    project_config_fields = {
        "name",
        "description",
        "annotator_guideline",
        "configuration",
        "annotations_per_doc",
        "annotator_max_annotation",
        "annotation_timeout",
        "document_input_preview"
    }


    @property
    def num_documents(self):
        return self.documents.count()

    @property
    def num_annotation_tasks_total(self):
        return self.documents.count() * self.annotations_per_doc

    @property
    def num_completed_tasks(self):
        return Annotation.objects.filter(document__project_id=self.pk, status=Annotation.COMPLETED).count()

    @property
    def num_pending_tasks(self):
        return Annotation.objects.filter(document__project_id=self.pk, status=Annotation.PENDING).count()

    @property
    def num_rejected_tasks(self):
        return Annotation.objects.filter(document__project_id=self.pk, status=Annotation.REJECTED).count()

    @property
    def num_timed_out_tasks(self):
        return Annotation.objects.filter(document__project_id=self.pk, status=Annotation.TIMED_OUT).count()

    @property
    def num_aborted_tasks(self):
        return Annotation.objects.filter(document__project_id=self.pk, status=Annotation.ABORTED).count()


    @property
    def is_project_configured(self):
        return len(self.configuration) > 0 and self.num_documents > 0

    @property
    def project_configuration_error_message(self):

        errors = []

        if len(self.configuration) < 1:
            errors.append("No annotation widgets defined in the configuration")

        if self.num_documents < 1:
            errors.append("No documents to annotate")

        return errors

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


    @property
    def num_annotators(self):
        return self.annotators.all().count()

    def add_annotator(self, user):
        self.annotators.add(user)
        self.save()

    def remove_annotator(self, user):
        self.annotators.remove(user)
        self.save()

        Annotation.clear_all_pending_user_annotations(user)

    def annotator_reached_quota(self, user):
        num_docs = self.documents.count()
        num_user_annotated_docs = 0
        for doc in self.documents.all():
            if doc.user_completed_annotation_of_document(user):
                num_user_annotated_docs += 1

        percentage_of_docs_annotated = num_user_annotated_docs / num_docs
        return percentage_of_docs_annotated >= self.annotator_max_annotation

    def get_current_annotator_task(self, user):

        current_annotations = user.annotations.filter(status=Annotation.PENDING)
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

    def get_project_stats(self):
        return {
            "owned_by": self.owner.username,
            "documents": self.num_documents,
            "completed_tasks": self.num_completed_tasks,
            "pending_tasks": self.num_pending_tasks,
            "rejected_tasks": self.num_rejected_tasks,
            "timed_out_tasks": self.num_timed_out_tasks,
            "aborted_tasks": self.num_aborted_tasks,
            "total_tasks": self.num_annotation_tasks_total,
            "is_configured": self.is_project_configured,
            "configuration_error": None if self.is_project_configured else self.project_configuration_error_message,
            "is_completed": self.is_completed,
            "num_annotators": self.num_annotators,
        }


class Document(models.Model):
    """
    Model to represent a document.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    data = models.JSONField(default=dict)
    created = models.DateTimeField(default=timezone.now)

    @property
    def num_completed_annotations(self):
        return self.annotations.filter(status=Annotation.COMPLETED).count()

    @property
    def num_rejected_annotations(self):
        return self.annotations.filter(status=Annotation.REJECTED).count()

    @property
    def num_timed_out_annotations(self):
        return self.annotations.filter(status=Annotation.TIMED_OUT).count()

    @property
    def num_pending_annotations(self):
        return self.annotations.filter(status=Annotation.PENDING).count()

    @property
    def num_aborted_annotations(self):
        return self.annotations.filter(status=Annotation.ABORTED).count()

    @property
    def num_completed_and_pending_annotations(self):
        return self.annotations.filter(
            Q(status=Annotation.COMPLETED) | Q(status=Annotation.PENDING)).count()

    def user_can_annotate_document(self, user):
        """ User must not have completed, pending or rejected the document"""
        num_user_annotation_in_doc = self.num_user_completed_annotations(user) + self.num_user_rejected_annotations(
            user) + self.num_user_pending_annotations(user)

        if num_user_annotation_in_doc > 1:
            raise RuntimeError(
                f"The user {user.username} has more than one annotation ({num_user_annotation_in_doc}) in the document.")

        return num_user_annotation_in_doc < 1

    def num_user_completed_annotations(self, user):
        return self.annotations.filter(user_id=user.pk, status=Annotation.COMPLETED).count()

    def num_user_pending_annotations(self, user):
        return self.annotations.filter(user_id=user.pk, status=Annotation.PENDING).count()

    def num_user_rejected_annotations(self, user):
        return self.annotations.filter(user_id=user.pk, status=Annotation.REJECTED).count()

    def num_user_timed_out_annotations(self, user):
        return self.annotations.filter(user_id=user.pk, status=Annotation.TIMED_OUT).count()

    def num_user_aborted_annotations(self, user):
        return self.annotations.filter(user_id=user.pk, status=Annotation.ABORTED).count()

    def user_completed_annotation_of_document(self, user):
        return self.num_user_completed_annotations(user) > 0


class Annotation(models.Model):
    """
    Model to represent a single annotation.
    """

    PENDING = 0
    COMPLETED = 1
    REJECTED = 2
    TIMED_OUT = 3
    ABORTED = 4

    ANNOTATION_STATUS = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (REJECTED, 'Rejected'),
        (TIMED_OUT, 'Timed out'),
        (ABORTED, 'Aborted')
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="annotations", null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="annotations")
    data = models.JSONField(default=dict)
    times_out_at = models.DateTimeField(default=None, null=True)
    created = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=ANNOTATION_STATUS, default=PENDING)
    status_time = models.DateTimeField(default=None, null=True)

    def get_annotation_task(self):
        document = self.document
        project = self.document.project
        return {
            "project_name": project.name,
            "project_description": project.description,
            "project_annotator_guideline": project.annotator_guideline,
            "project_config": project.configuration,
            "project_id": project.pk,
            "document_id": document.pk,
            "document_data": document.data,
            "annotation_id": self.pk,
            "annotation_timeout": self.times_out_at
        }

    def _set_new_status(self, status, time=timezone.now()):
        self.ensure_status_pending()
        self.status = status
        self.status_time = time


    def complete_annotation(self, data, time=timezone.now()):
        self.data = data
        self._set_new_status(Annotation.COMPLETED, time)
        self.save()

        # Also check whether the project has been completed
        self.document.project.check_project_complete()

    def reject_annotation(self, time=timezone.now()):
        self._set_new_status(Annotation.REJECTED, time)
        self.save()

    def timeout_annotation(self, time=timezone.now()):
        self._set_new_status(Annotation.TIMED_OUT, time)
        self.save()

    def abort_annotation(self, time=timezone.now()):
        self._set_new_status(Annotation.ABORTED, time)
        self.save()


    def ensure_status_pending(self):
        if self.status == Annotation.PENDING and self.status_time is None:
            # Ok if still pending and doesn't have status time
            return

        if self.status == Annotation.COMPLETED:
            log.warning(f"Annotation id {self.id} is already completed.")
            raise RuntimeError("The annotation is already completed.")

        if self.status == Annotation.REJECTED:
            log.warning(f"Annotation id {self.id} is already rejected.")
            raise RuntimeError("The annotation is already rejected.")

        if self.status == Annotation.TIMED_OUT:
            log.warning(f"Annotation id {self.id} is already timed out.")
            raise RuntimeError("The annotation is already timed out.")

        if self.status == Annotation.ABORTED:
            log.warning(f"Annotation id {self.id} is already aborted.")
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
        timed_out_annotations = Annotation.objects.filter(times_out_at__lt=current_time, status=Annotation.PENDING)
        for annotation in timed_out_annotations:
            annotation.timeout_annotation(current_time)

        return len(timed_out_annotations)

    @staticmethod
    def clear_all_pending_user_annotations(user):
        pending_annotations = Annotation.objects.filter(user_id=user.pk, status=Annotation.PENDING)

        if pending_annotations.count() > 1:
            raise RuntimeError("More than one pending annotation has been created for the user")

        for annotation in pending_annotations:
            annotation.abort_annotation()


