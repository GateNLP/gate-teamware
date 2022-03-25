import math

from django.conf import settings
import logging
import django
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.db.models import Q, F, Count

from backend.utils.misc import get_value_from_key_path, insert_value_to_key_path

log = logging.getLogger(__name__)


class ServiceUser(AbstractUser):
    """
    Custom user class.
    """
    
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
    
        if self.annotations.filter(document_id=document.pk).count() > 0:
            return True

        if self.annotates:
            if not self.annotates.filter(pk=document.project.pk).first():
                return False

            if self.annotates.filter(pk=document.project.pk).first().documents.count() > 0:
                return True
        
        else:
            # If user is no longer active on a project, but has annotations from that project, this should have been caught above
            return False


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
    allow_document_reject = models.BooleanField(default=True)
    annotation_timeout = models.IntegerField(default=60)
    document_input_preview = models.JSONField(default=default_document_input_preview)
    document_id_field = models.TextField(default="name")
    annotators = models.ManyToManyField(get_user_model(), through='AnnotatorProject', related_name="annotates")
    has_training_stage = models.BooleanField(default=False)
    has_test_stage = models.BooleanField(default=False)
    can_annotate_after_passing_test = models.BooleanField(default=True)
    min_test_pass_threshold = models.FloatField(default=1.0, null=True)
    document_gold_standard_field = models.TextField(default="gold")

    project_config_fields = {
        "name",
        "description",
        "annotator_guideline",
        "configuration",
        "annotations_per_doc",
        "annotator_max_annotation",
        "allow_document_reject",
        "annotation_timeout",
        "document_input_preview",
        "document_id_field",
        "allow_document_reject",
    }


    @property
    def num_documents(self):
        return self.documents.filter(doc_type=Document.ANNOTATION).count()

    @property
    def num_test_documents(self):
        return self.documents.filter(doc_type=Document.TEST).count()

    @property
    def num_training_documents(self):
        return self.documents.filter(doc_type=Document.TRAINING).count()

    @property
    def num_annotation_tasks_total(self):
        return self.num_documents * self.annotations_per_doc

    @property
    def num_completed_tasks(self):
        return self._get_project_annotations_query(status=Annotation.COMPLETED).count()

    @property
    def num_pending_tasks(self):
        return self._get_project_annotations_query(status=Annotation.PENDING).count()

    @property
    def num_rejected_tasks(self):
        return self._get_project_annotations_query(status=Annotation.REJECTED).count()

    @property
    def num_timed_out_tasks(self):
        return self._get_project_annotations_query(status=Annotation.TIMED_OUT).count()

    @property
    def num_aborted_tasks(self):
        return Annotation.objects.filter(document__project_id=self.pk, status=Annotation.ABORTED).count()



    @property
    def num_occupied_tasks(self):
        return (self._get_project_annotations_query(Annotation.COMPLETED) |
                self._get_project_annotations_query(Annotation.PENDING)).count()

    @property
    def num_annotation_tasks_remaining(self):
        return self.num_annotation_tasks_total - self.num_occupied_tasks

    def _get_project_annotations_query(self, status=None):
        if status is None:
            return Annotation.objects.filter(document__project_id=self.pk)
        else:
            return Annotation.objects.filter(document__project_id=self.pk, status=status)

    @property
    def is_completed(self):
        # Project must have documents to be completed
        if self.num_annotation_tasks_total <= 0:
            return False

        return self.num_annotation_tasks_total - self.num_completed_tasks < 1

    @property
    def max_num_task_per_annotator(self):
        return math.ceil(self.annotator_max_annotation * self.documents.all().count())

    @property
    def num_annotators(self):
        return self.annotators.filter(annotatorproject__status=AnnotatorProject.ACTIVE).count()

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

    def add_annotator(self, user):
        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)
        except ObjectDoesNotExist:
            annotator_project = AnnotatorProject(annotator=user, project=self)
            annotator_project.save()

        annotator_project.set_status(AnnotatorProject.ACTIVE)


    def remove_annotator(self, user):
        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)
            annotator_project.set_status(AnnotatorProject.COMPLETED) 
        except ObjectDoesNotExist:
            pass

        Annotation.clear_all_pending_user_annotations(user)

    def num_annotator_task_remaining(self, user):

        num_annotable = self.get_annotator_annotatable_documents_query(user).count()
        num_completed_by_user = self.get_annotator_completed_documents_query(user).count()
        max_num_docs_user_can_annotate = self.max_num_task_per_annotator
        remaining_docs_in_quota = max_num_docs_user_can_annotate - num_completed_by_user

        if remaining_docs_in_quota < num_annotable:
            return remaining_docs_in_quota
        else:
            return num_annotable

    def get_annotator_annotatable_documents_query(self, user):
        # Filter to get the count of occupied annotations in the document
        # (annotations with COMPLETED and PENDING status)
        occupied_filter = (Q(annotations__status=Annotation.COMPLETED) |
                           Q(annotations__status=Annotation.PENDING))
        occupied_count = Count('annotations', filter=occupied_filter)

        # Filter to get the count of user occupied annotation in the document
        # (annotations with COMPLETED, PENDING, and REJECTED status)
        user_occupied_filter = (Q(annotations__user_id=user.pk, annotations__status=Annotation.COMPLETED) |
                                Q(annotations__user_id=user.pk, annotations__status=Annotation.PENDING) |
                                Q(annotations__user_id=user.pk, annotations__status=Annotation.REJECTED))
        user_occupied_count = Count('annotations', filter=user_occupied_filter)

        # All remaining documents that user can annotate
        annotatable_docs = Document.objects.filter(project_id=self.pk) \
            .annotate(num_occupied=occupied_count) \
            .annotate(num_user_occupied=user_occupied_count) \
            .filter(num_occupied__lt=self.annotations_per_doc, num_user_occupied__lt=1)

        return annotatable_docs

    def get_annotator_occupied_documents_query(self, user):
        # Filter to get the count of user occupied annotation in the document
        # (annotations with COMPLETED, PENDING, and REJECTED status)
        user_occupied_filter = (Q(annotations__user_id=user.pk, annotations__status=Annotation.COMPLETED) |
                                Q(annotations__user_id=user.pk, annotations__status=Annotation.PENDING) |
                                Q(annotations__user_id=user.pk, annotations__status=Annotation.REJECTED))
        user_occupied_count = Count('annotations', filter=user_occupied_filter)

        # Number of user annotated docs in the project
        occupied_docs = Document.objects \
            .annotate(num_user_occupied=user_occupied_count) \
            .filter(project_id=self.pk, num_user_occupied__gt=0)

        return occupied_docs

    def get_annotator_completed_documents_query(self, user):
        # Filter to get the count of user occupied annotation in the document
        # (annotations with COMPLETED, PENDING, and REJECTED status)
        completed_filter = (Q(annotations__user_id=user.pk, annotations__status=Annotation.COMPLETED))
        completed_count = Count('annotations', filter=completed_filter)

        # Number of user completed annotated docs in the project
        completed_docs = Document.objects \
            .annotate(num_user_occupied=completed_count) \
            .filter(project_id=self.pk, num_user_occupied__gt=0)

        return completed_docs

    def get_annotator_pending_documents_query(self, user):
        # Filter to get the count of user occupied annotation in the document
        # (annotations with COMPLETED, PENDING, and REJECTED status)
        pending_filter = (Q(annotations__user_id=user.pk, annotations__status=Annotation.PENDING))
        pending_count = Count('annotations', filter=pending_filter)

        # Number of user completed annotated docs in the project
        pending_docs = Document.objects \
            .annotate(num_user_occupied=pending_count) \
            .filter(project_id=self.pk, num_user_occupied__gt=0)

        return pending_docs


    def get_annotator_task(self, user):
        """
        Gets or creates a new annotation task for user (annotator). Returns None and removes
        user from annotator list if there's no more tasks.
        """

        # User has existing task
        annotation = self.get_current_annotator_task(user)

        # Generate new task if there's no existing task and user has not reached quota
        if not annotation and not self.annotator_reached_quota(user):
            annotation = self.assign_annotator_task(user)

        # Returns annotation task dict or remove user from project if there's no task
        if annotation:
            return self.get_annotation_task_dict(annotation)
        else:
            # If there's no new annotation task then remove user from project
            self.remove_annotator(user)
            return None

    def annotator_reached_quota(self, user):

        num_user_annotated_docs = (self.get_annotator_completed_documents_query(user) |
                                   self.get_annotator_pending_documents_query(user)).count()

        return num_user_annotated_docs >= self.max_num_task_per_annotator

    def get_current_annotator_task(self, user):
        """
        Gets annotator's current pending task in the project.
        """

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

    def get_annotation_task_dict(self, annotation):
        document = annotation.document
        return {
            "project_name": self.name,
            "project_description": self.description,
            "project_annotator_guideline": self.annotator_guideline,
            "project_config": self.configuration,
            "project_id": self.pk,
            "document_id": document.pk,
            "document_field_id": get_value_from_key_path(document.data, self.document_id_field),
            "document_data": document.data,
            "annotation_id": annotation.pk,
            "allow_document_reject": self.allow_document_reject,
            "annotation_timeout": annotation.times_out_at,
            "annotator_remaining_tasks": self.num_annotator_task_remaining(user=annotation.user),
            "annotator_completed_tasks": self.get_annotator_completed_documents_query(user=annotation.user).count()
        }

    def assign_annotator_task(self, user):
        """
        Assign an available annotation task to a user
        """

        if self.num_annotation_tasks_remaining > 0:
            for doc in self.documents.order_by('?').all():
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

    def get_annotators_dict(self):
        return {
            "annotators": [{"id":ann.id, "username":ann.username, "email":ann.email} for ann in self.annotators.filter(annotatorproject__status=AnnotatorProject.ACTIVE).all()]
        }

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

class AnnotatorProject(models.Model):
    """
    Intermediate class to represent annotator-project relationship
    """
    ACTIVE = 0
    COMPLETED = 1

    STATUS = (
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed')
    )

    annotator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    training_score = models.FloatField(null=True)
    test_score = models.FloatField(null=True)
    training_completed = models.DateTimeField(null=True)
    test_completed = models.DateTimeField(null=True)
    annotations_completed = models.DateTimeField(null=True)
    status = models.IntegerField(choices=STATUS, default=ACTIVE)
    rejected = models.BooleanField(default=False)
    
    @property
    def num_annotations(self):
        # Is this better as a prop method or as a normal property?
        pass

    def set_status(self, status):
        self.status = status
        self.save()

class Document(models.Model):
    """
    Model to represent a document.
    """

    ANNOTATION = 0
    TRAINING = 1
    TEST = 2

    DOCUMENT_TYPE = (
        (ANNOTATION, 'Annotation'),
        (TRAINING, 'Training'),
        (TEST, 'Test')
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    data = models.JSONField(default=dict)
    created = models.DateTimeField(default=timezone.now)
    doc_type = models.IntegerField(choices=DOCUMENT_TYPE, default=ANNOTATION)

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
        num_user_annotation_in_doc = self.annotations.filter(
            Q(user_id=user.pk, status=Annotation.COMPLETED) |
            Q(user_id=user.pk, status=Annotation.PENDING) |
            Q(user_id=user.pk, status=Annotation.REJECTED)).count()

        if num_user_annotation_in_doc > 1:
            raise RuntimeError(
                f"The user {user.username} has more than one annotation ({num_user_annotation_in_doc}) in the document.")

        return (num_user_annotation_in_doc < 1 and
                self.num_completed_and_pending_annotations < self.project.annotations_per_doc)

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

    def get_listing(self, annotation_list=[]):
        """
        Get minimal dictionary representation of document for rendering an object list
        """
        doc_out = {
            "id": self.pk,
            "annotations": annotation_list,
            "created": self.created,
            "completed": self.num_completed_annotations,
            "rejected": self.num_rejected_annotations,
            "timed_out": self.num_timed_out_annotations,
            "pending": self.num_pending_annotations,
            "aborted": self.num_aborted_annotations,
            "doc_id": get_value_from_key_path(self.data, self.project.document_id_field),
            "project_id": self.project.id
        }

        return doc_out

    def get_doc_annotation_dict(self, json_format="raw"):
        """
        Get dictionary of document and its annotations for export
        """

        # Create dictionary for document
        doc_dict = None
        if json_format == "raw" or json_format == "csv":
            doc_dict = self.data
        elif json_format == "gate":

            ignore_keys = {"text", self.project.document_id_field}
            features_dict = {key: value for key, value in self.data.items() if key not in ignore_keys}

            doc_dict = {
                "text": self.data["text"],
                "features": features_dict,
                "offset_type": "p",
                "name": get_value_from_key_path(self.data, self.project.document_id_field)
            }
            pass

        # Insert annotation sets into the doc dict
        annotations = self.annotations.filter(status=Annotation.COMPLETED)
        if json_format == "csv":
            # Format annotations for CSV export
            annotation_sets = {}
            for annotation in annotations:
                a_data = annotation.data
                annotation_dict = {}
                # Format for csv, flatten list values
                for a_key, a_value in a_data.items():
                    if isinstance(a_value, list):
                        annotation_dict[a_key] = ",".join(a_value)
                    else:
                        annotation_dict[a_key] = a_value
                annotation_dict["duration_seconds"] = annotation.time_to_complete
                annotation_sets[annotation.user.username] = annotation_dict

            doc_dict["annotations"] = annotation_sets

        else:
            # Format for JSON in line with GATE formatting
            annotation_sets = {}
            for annotation in annotations:
                a_data = annotation.data
                annotation_set = {
                    "name": annotation.user.username,
                    "annotations": [
                        {
                            "type": "Document",
                            "start": 0,
                            "end": 0,
                            "id": 0,
                            "duration_seconds": annotation.time_to_complete,
                            "features": {
                                "label": a_data
                            }
                        }
                    ],
                    "next_annid": 1,
                }
                annotation_sets[annotation.user.username] = annotation_set
            doc_dict["annotation_sets"] = annotation_sets

        return doc_dict

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
    time_to_complete = models.FloatField(default=None, null=True)


    def _set_new_status(self, status, time=timezone.now()):
        self.ensure_status_pending()
        self.status = status
        self.status_time = time


    def complete_annotation(self, data, elapsed_time=None, time=timezone.now()):
        self.data = data
        self._set_new_status(Annotation.COMPLETED, time)
        self.time_to_complete = elapsed_time
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

    def get_listing(self):
        return {
            "id": self.pk,
            "annotated_by": self.user.username,
            "created": self.created,
            "completed": self.status_time if self.status == Annotation.COMPLETED else None,
            "rejected": self.status_time if self.status == Annotation.REJECTED else None,
            "timed_out": self.status_time if self.status == Annotation.TIMED_OUT else None,
            "aborted": self.status_time if self.status == Annotation.ABORTED else None,
            "times_out_at": self.times_out_at
        }

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


