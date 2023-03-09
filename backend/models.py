import math
import uuid

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
from backend.utils.telemetry import TelemetrySender

log = logging.getLogger(__name__)

class UserDocumentFormatPreference:
    JSON = 0
    CSV = 1

    USER_DOC_FORMAT_PREF = (
        (JSON, 'JSON'),
        (CSV, 'CSV')
    )

class DocumentType:
    ANNOTATION = 0
    TRAINING = 1
    TEST = 2

    DOCUMENT_TYPE = (
        (ANNOTATION, 'Annotation'),
        (TRAINING, 'Training'),
        (TEST, 'Test')
    )


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
    doc_format_pref = models.IntegerField(choices=UserDocumentFormatPreference.USER_DOC_FORMAT_PREF,
                                          default=UserDocumentFormatPreference.JSON)
    agreed_privacy_policy = models.BooleanField(default=False)

    @property
    def has_active_project(self):
        return self.annotatorproject_set.filter(status=AnnotatorProject.ACTIVE).count() > 0

    @property
    def active_project(self):
        """
        Gets the project that user's currently active in
        :returns: Project object that user's active in, None if not active in any project
        """
        active_annotator_project = self.annotatorproject_set.filter(status=AnnotatorProject.ACTIVE).first()
        if active_annotator_project:
            return active_annotator_project.project

        return None

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

    def is_manager_or_above(self):
        if self.is_manager or self.is_staff or self.is_superuser:
            return True
        else:
            return False


def default_document_input_preview():
    return {"text": "<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>"}


class Project(models.Model):
    """
    Model to store annotation projects.
    """
    name = models.TextField(default="New project")
    uuid = models.UUIDField(primary_key = False, default = uuid.uuid4, editable = False)
    description = models.TextField(default="")
    annotator_guideline = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    configuration = models.JSONField(default=list)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="owns")
    annotations_per_doc = models.IntegerField(default=3)
    annotator_max_annotation = models.FloatField(default=0.6)
    # Allow annotators to reject document
    allow_document_reject = models.BooleanField(default=True)
    # Allow annotators to change their annotation after it's been submitted
    allow_annotation_change = models.BooleanField(default=True)
    # Time it takes for user annotation to timeout (minutes)
    annotation_timeout = models.IntegerField(default=60)
    # Stores a document that's used for previewing in the AnnotationRenderer
    document_input_preview = models.JSONField(default=default_document_input_preview)
    # Stores a csv document that's used for previewing in the AnnotationRenderer
    document_input_preview_csv = models.TextField(default="")
    document_id_field = models.TextField(default="name")
    annotators = models.ManyToManyField(get_user_model(), through='AnnotatorProject', related_name="annotates")
    has_training_stage = models.BooleanField(default=False)
    has_test_stage = models.BooleanField(default=False)
    can_annotate_after_passing_training_and_test = models.BooleanField(default=True)
    min_test_pass_threshold = models.FloatField(default=1.0, null=True)
    document_gold_standard_field = models.TextField(default="gold")
    document_pre_annotation_field = models.TextField(default="")

    @classmethod
    def get_project_config_fields(cls, exclude_fields: set = set()):
        exclude_field_types = {
            models.ManyToOneRel,
            models.ManyToManyField,
            models.ManyToManyRel,
        }
        fields = Project._meta.get_fields()
        config_fields = []

        for field in fields:
            if field.__class__ not in exclude_field_types and field.name not in exclude_fields:
                config_fields.append(field)

        return config_fields

    @classmethod
    def get_project_export_field_names(cls):
        fields = Project.get_project_config_fields({"owner", "id", "created", "uuid"})
        return [field.name for field in fields]


    def clone(self, new_name = None, clone_name_prefix="Copy of ", owner = None):
        """
        Clones the Project object, does not retain documents and annotator membership
        """
        exclude_fields = { "name", "owner", "id", "created", "uuid" }

        # Setting project name
        new_project_name = new_name if new_name is not None else ""
        if clone_name_prefix:
            new_project_name = clone_name_prefix + self.name
        new_project = Project.objects.create(name=new_project_name)
        # Setting owner
        new_project.owner = owner
        # Copy all config over
        config_fields = self.get_project_config_fields(exclude_fields)
        for field in config_fields:
            setattr(new_project, field.name, getattr(self, field.name))

        new_project.save()
        return new_project


    @property
    def num_documents(self):
        return self.documents.filter(doc_type=DocumentType.ANNOTATION).count()

    @property
    def num_test_documents(self):
        return self.documents.filter(doc_type=DocumentType.TEST).count()

    @property
    def num_training_documents(self):
        return self.documents.filter(doc_type=DocumentType.TRAINING).count()

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
        return Annotation.objects.filter(document__project_id=self.pk,
                                         status=Annotation.ABORTED,
                                         document__doc_type=DocumentType.ANNOTATION).count()

    @property
    def num_occupied_tasks(self):
        return (self._get_project_annotations_query(Annotation.COMPLETED) |
                self._get_project_annotations_query(Annotation.PENDING)).count()

    @property
    def num_annotation_tasks_remaining(self):
        return self.num_annotation_tasks_total - self.num_occupied_tasks

    def _get_project_annotations_query(self, status=None, doc_type=DocumentType.ANNOTATION):
        if status is None:
            return Annotation.objects.filter(document__project_id=self.pk,
                                             document__doc_type=doc_type)
        else:
            return Annotation.objects.filter(document__project_id=self.pk,
                                             status=status,
                                             document__doc_type=doc_type)

    @property
    def is_completed(self):
        # Project must have documents to be completed
        if self.num_annotation_tasks_total <= 0:
            return False

        return self.num_annotation_tasks_total - self.num_completed_tasks < 1

    @property
    def max_num_task_per_annotator(self):
        return math.ceil(
            self.annotator_max_annotation * self.documents.filter(doc_type=DocumentType.ANNOTATION).count())

    @property
    def num_annotators(self):
        return self.annotators.filter(annotatorproject__status=AnnotatorProject.ACTIVE).count()

    @property
    def num_all_annotators(self) -> int:
        """Count of all annotators associated with project."""
        return self.annotators.filter().count()

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

    def delete(self):
        """
        Overloaded delete method to optionally send project telemetry stats prior to deletion.
        """

        try:
            if settings.TELEMETRY_ON and self.num_all_annotators > 0:
                self.send_telemetry("deleted")

        finally:
            super().delete()

    def add_annotator(self, user):

        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)
        except ObjectDoesNotExist:
            allowed_to_annotate = not self.has_test_stage and not self.has_training_stage
            annotator_project = AnnotatorProject.objects.create(annotator=user,
                                                                project=self,
                                                                status=AnnotatorProject.ACTIVE,
                                                                allowed_to_annotate=allowed_to_annotate)

        return annotator_project

    def make_annotator_active(self, user):
        """
        Makes the user active in the project again. An user can be made inactive from the project as a
        result of completing all annotation task, manager marking them as completed the project,
        rejecting them from the project or the user has left the project themselves.
        """

        # Check that user is not active in another project
        active_project = user.active_project

        if active_project == self:
            raise Exception("User already active in this project")

        if active_project is not None:
            raise Exception(f"User is already active in project {active_project.name}")

        if self.annotator_reached_quota(user):
            raise Exception(f"User is already reached annotation quota")

        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)
            annotator_project.status = AnnotatorProject.ACTIVE
            annotator_project.rejected = False
            annotator_project.save()
        except ObjectDoesNotExist:
            raise Exception("User must be added to the project before they can be made active.")

    def annotator_completed_training(self, user, finished_time=timezone.now()):
        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)
            annotator_project.training_completed = finished_time
            annotator_project.training_score = self.get_annotator_document_score(user, DocumentType.TRAINING)

            if annotator_project.project.can_annotate_after_passing_training_and_test and not annotator_project.project.has_test_stage:
                annotator_project.allowed_to_annotate = True

            annotator_project.save()
        except ObjectDoesNotExist:
            raise Exception(f"User {user.username} is not an annotator of the project.")

    def get_annotator_document_score(self, user, doc_type):
        test_docs = self.documents.filter(doc_type=doc_type)

        score = 0

        for document in test_docs:
            # Checks answers for all test documents
            user_annotations = document.annotations.filter(user_id=user.pk)
            if user_annotations.count() > 1:
                # User should not have more than 1 annotation per document
                raise Exception(f"User {user.username} has more than 1 annotation in document")

            annotation = user_annotations.first()

            # Skip if there's no annotation
            if not annotation:
                continue

            # Check that answer key exists in document
            answers = get_value_from_key_path(document.data, self.document_gold_standard_field)
            if answers is None:
                raise Exception(f"No gold standard (answer) field inside test document")

            if self.check_annotation_answer(annotation.data, answers):
                score += 1

        return score

    def check_annotation_answer(self, annotation_data, answers):
        """
        Compare answers between the annotation.data and document's gold standard field with answers
        """

        is_correct = True
        for label in answers:
            if label not in annotation_data:
                return False  # Label does not exist in annotation

            annotation_val = annotation_data[label]
            answer_val = answers[label]["value"]
            if isinstance(annotation_val, str) and isinstance(answer_val, str):
                if annotation_val != answer_val:
                    is_correct = False
            elif isinstance(annotation_val, list) and isinstance(answer_val, list):
                comparison_set = set(annotation_val) & set(answer_val)
                if len(answer_val) != len(annotation_val) or len(comparison_set) != len(answer_val):
                    is_correct = False
            else:
                is_correct = False

        return is_correct

    def annotator_completed_test(self, user, finished_time=timezone.now()):
        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)
            annotator_project.test_completed = finished_time
            annotator_project.test_score = self.get_annotator_document_score(user, DocumentType.TEST)
            annotator_test_score_proportion = annotator_project.test_score / self.num_test_documents if self.num_test_documents > 0 else 0
            if self.can_annotate_after_passing_training_and_test and \
                    annotator_test_score_proportion >= self.min_test_pass_threshold:
                annotator_project.allowed_to_annotate = True

            annotator_project.save()

        except ObjectDoesNotExist:
            raise Exception(f"User {user.username} is not an annotator of the project.")

    def annotator_set_allowed_to_annotate(self, user, finished_time=timezone.now()):
        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)

            annotator_project.allowed_to_annotate = True
            annotator_project.save()

        except ObjectDoesNotExist:
            raise Exception(f"User {user.username} is not an annotator of the project.")

    def reject_annotator(self, user, finished_time=timezone.now()):
        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)
            annotator_project.annotations_completed = finished_time
            annotator_project.status = AnnotatorProject.COMPLETED
            annotator_project.rejected = True
            annotator_project.save()
        except ObjectDoesNotExist:
            raise Exception(f"User {user.username} is not an annotator of the project.")

    def remove_annotator(self, user, finished_time=timezone.now()):
        try:
            annotator_project = AnnotatorProject.objects.get(project=self, annotator=user)
            annotator_project.annotations_completed = finished_time
            annotator_project.status = AnnotatorProject.COMPLETED
            annotator_project.save()

            Annotation.clear_all_pending_user_annotations(user)

        except ObjectDoesNotExist:
            raise Exception(f"User {user.username} is not an annotator of the project.")

    def num_annotator_task_remaining(self, user):

        num_annotable = self.get_annotator_annotatable_documents_query(user).count()
        num_completed_by_user = self.get_annotator_completed_documents_query(user).count()
        max_num_docs_user_can_annotate = self.max_num_task_per_annotator
        remaining_docs_in_quota = max_num_docs_user_can_annotate - num_completed_by_user

        if remaining_docs_in_quota < num_annotable:
            return remaining_docs_in_quota
        else:
            return num_annotable

    def get_annotator_annotatable_documents_query(self, user, doc_type=DocumentType.ANNOTATION):
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
        annotatable_docs = Document.objects.filter(project_id=self.pk, doc_type=doc_type) \
            .annotate(num_occupied=occupied_count) \
            .annotate(num_user_occupied=user_occupied_count) \
            .filter(num_occupied__lt=self.annotations_per_doc, num_user_occupied__lt=1)

        return annotatable_docs

    def get_annotator_occupied_documents_query(self, user, doc_type=DocumentType.ANNOTATION):
        # Filter to get the count of user occupied annotation in the document
        # (annotations with COMPLETED, PENDING, and REJECTED status)
        user_occupied_filter = (Q(annotations__user_id=user.pk, annotations__status=Annotation.COMPLETED) |
                                Q(annotations__user_id=user.pk, annotations__status=Annotation.PENDING) |
                                Q(annotations__user_id=user.pk, annotations__status=Annotation.REJECTED))
        user_occupied_count = Count('annotations', filter=user_occupied_filter)

        # Number of user annotated docs in the project
        occupied_docs = Document.objects.filter(project_id=self.pk, doc_type=doc_type) \
            .annotate(num_user_occupied=user_occupied_count) \
            .filter(num_user_occupied__gt=0)

        return occupied_docs

    def get_annotator_completed_documents_query(self, user, doc_type=DocumentType.ANNOTATION):
        # Filter to get the count of user occupied annotation in the document
        # (annotations with COMPLETED, PENDING, and REJECTED status)
        completed_filter = (Q(annotations__user_id=user.pk, annotations__status=Annotation.COMPLETED))
        completed_count = Count('annotations', filter=completed_filter)

        # Number of user completed annotated docs in the project
        completed_docs = Document.objects.filter(project_id=self.pk, doc_type=doc_type) \
            .annotate(num_user_occupied=completed_count) \
            .filter(num_user_occupied__gt=0)

        return completed_docs

    def get_annotator_pending_documents_query(self, user, doc_type=DocumentType.ANNOTATION):
        # Filter to get the count of user occupied annotation in the document
        # (annotations with COMPLETED, PENDING, and REJECTED status)
        pending_filter = (Q(annotations__user_id=user.pk, annotations__status=Annotation.PENDING))
        pending_count = Count('annotations', filter=pending_filter)

        # Number of user completed annotated docs in the project
        pending_docs = Document.objects.filter(project_id=self.pk, doc_type=doc_type) \
            .annotate(num_user_occupied=pending_count) \
            .filter(num_user_occupied__gt=0)

        return pending_docs

    def get_annotator_task(self, user):
        """
        Gets or creates a new annotation task for user (annotator).

        :returns: Dictionary with all information to complete an annotation task. Only project information
            is returned if user is waiting to be approved as an annotator. Returns None and removes
            user from annotator list if there's no more tasks or user reached quota.
        """

        annotation = self.get_current_annotator_task(user)
        if annotation:
            # User has existing task
            return self.get_annotation_task_dict(annotation)
        else:
            # Tries to generate new task if there's no existing task
            if self.annotator_reached_quota(user):
                self.remove_annotator(user)
                return None  # Also return None as we've completed all the task
            else:
                return self.decide_annotator_task_type_and_assign(user)

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

    def get_annotation_task_dict(self, annotation, include_task_history_in_project=True):
        """
        Returns a dictionary with all information required rendering an annotation task
        annotation:Annotation - The annotation to create an annotation task dictionary for
        task_history_in_project:bool - Returns a list of annotation ids for this user in the project
        """
        document = annotation.document

        output = {
            **self.get_annotation_task_project_dict(),
            "document_id": document.pk,
            "document_field_id": get_value_from_key_path(document.data, self.document_id_field),
            "document_data": document.data,
            "document_type": document.doc_type_str,
            "annotation_id": annotation.pk,
            "annotation_data": annotation.data,
            "allow_document_reject": self.allow_document_reject,
            "annotation_timeout": annotation.times_out_at,
            "annotator_remaining_tasks": self.num_annotator_task_remaining(user=annotation.user),
            "annotator_completed_tasks": self.get_annotator_completed_documents_query(user=annotation.user).count(),
            "annotator_completed_training_tasks": self.get_annotator_completed_documents_query(user=annotation.user,
                                                                                               doc_type=DocumentType.TRAINING).count(),
            "annotator_completed_test_tasks": self.get_annotator_completed_documents_query(user=annotation.user,
                                                                                           doc_type=DocumentType.TEST).count(),
            "document_gold_standard_field": self.document_gold_standard_field,
            "document_pre_annotation_field": self.document_pre_annotation_field,
        }

        if include_task_history_in_project and document.doc_type is DocumentType.ANNOTATION:
            # If specified, also returns a list of annotation ids for this user in the project
            output["task_history"] = [annotation.pk for annotation in
                                      Annotation.get_annotations_for_user_in_project(annotation.user.pk, self.pk)]

        return output

    def get_annotation_task_project_dict(self):

        return {
            "project_name": self.name,
            "project_description": self.description,
            "project_annotator_guideline": self.annotator_guideline,
            "project_config": self.configuration,
            "project_id": self.pk,
        }

    def decide_annotator_task_type_and_assign(self, user):
        """
        Assign an available annotation task to a user
        """

        # Check annotator's current status in the project
        annotator_proj = AnnotatorProject.objects.get(annotator=user, project=self)

        # Check annotator's current status in the project
        if not annotator_proj.allowed_to_annotate:
            # Check whether annotator is in test or training
            if self.has_training_stage and not annotator_proj.training_completed:
                # Check whether the annotator's completed all training tasks, mark complete if so
                if self.get_annotator_annotatable_documents_query(user, doc_type=DocumentType.TRAINING).count() == 0:
                    self.annotator_completed_training(user)

            if self.has_test_stage and not annotator_proj.test_completed:
                # Check whether annotator's completed all test tasks, mark complete if so
                if self.get_annotator_annotatable_documents_query(user, doc_type=DocumentType.TEST).count() == 0:
                    self.annotator_completed_test(user)

        # Refresh object to ensure the phase changes are picked up
        annotator_proj.refresh_from_db()

        # Assign task
        if annotator_proj.allowed_to_annotate:
            # If allowed to annotate then skip over testing and training stage
            annotation = self.assign_annotator_task(user)
            if annotation:
                return self.get_annotation_task_dict(annotation)
            else:
                # Remove annotator from project if there's no more tasks
                annotator_proj.annotations_completed = timezone.now()
                annotator_proj.save()
                self.remove_annotator(user)
                return None
        elif self.has_training_stage and not annotator_proj.training_completed:
            # Tries to assign training task
            return self.get_annotation_task_dict(self.assign_annotator_task(user, DocumentType.TRAINING))
        elif self.has_test_stage and not annotator_proj.test_completed:
            # Tries to assign test task
            return self.get_annotation_task_dict(self.assign_annotator_task(user, DocumentType.TEST))
        else:
            return self.get_annotation_task_project_dict()

    def assign_annotator_task(self, user, doc_type=DocumentType.ANNOTATION):
        """
        Assigns an annotation task to the annotator, works for testing, training and annotation tasks.
        Annotation task performs an extra check for remaining annotation task (num_annotation_tasks_remaining),
        testing and training does not do this check as the annotator must annotate all documents.
        """
        if (DocumentType.ANNOTATION and self.num_annotation_tasks_remaining > 0) or \
                DocumentType.TEST or DocumentType.TRAINING:
            for doc in self.documents.filter(doc_type=doc_type).order_by('?'):
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
        """
        Checks that all annotations have been completed, release all annotators from project.
        If complete, also send telemetry data.
        """
        if self.is_completed:
            for annotator in self.annotators.all():
                self.remove_annotator(annotator)
            if settings.TELEMETRY_ON:
                self.send_telemetry(status="complete")

    def send_telemetry(self, status:str):
        """
        Sends telemetry data for the project depending on the status.
        """
        if settings.TELEMETRY_ON:
            ts = TelemetrySender(status=status, data=self.get_telemetry_stats())
            ts.send()

    def get_annotators_dict(self):
        return {
            "annotators": [{"id": ann.id, "username": ann.username, "email": ann.email} for ann in
                           self.annotators.filter(annotatorproject__status=AnnotatorProject.ACTIVE).all()]
        }

    def get_project_stats(self):
        return {
            "owned_by": self.owner.username,
            "documents": self.num_documents,
            "training_documents": self.num_training_documents,
            "test_documents": self.num_test_documents,
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

    def get_telemetry_stats(self) -> dict:
        """
        Returns a dict of stats specifically for telemetry including no identifying information.
        """
        return {
            "uuid": str(self.uuid),
            "documents": self.num_documents,
            "training_documents": self.num_training_documents,
            "test_documents": self.num_test_documents,
            "completed_tasks": self.num_completed_tasks,
            "pending_tasks": self.num_pending_tasks,
            "rejected_tasks": self.num_rejected_tasks,
            "timed_out_tasks": self.num_timed_out_tasks,
            "aborted_tasks": self.num_aborted_tasks,
            "total_tasks": self.num_annotation_tasks_total,
            "is_configured": self.is_project_configured,
            "is_completed": self.is_completed,
            "num_annotators": self.num_all_annotators,
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
    training_score = models.FloatField(default=0)
    test_score = models.FloatField(default=0)
    training_completed = models.DateTimeField(null=True)
    test_completed = models.DateTimeField(null=True)
    annotations_completed = models.DateTimeField(null=True)
    allowed_to_annotate = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS, default=ACTIVE)
    rejected = models.BooleanField(default=False)

    @property
    def num_annotations(self):
        """Number of annotations completed by this annotator in this project"""
        count = 0
        for d in self.project.documents.filter(doc_type=DocumentType.ANNOTATION):
            count += d.annotations.filter(user=self.annotator).count()
        return count

    def set_status(self, status):
        self.status = status
        self.save()

    def get_stats(self):
        return {
            "annotations": self.num_annotations,
        }


class Document(models.Model):
    """
    Model to represent a document.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    data = models.JSONField(default=dict)
    created = models.DateTimeField(default=timezone.now)
    doc_type = models.IntegerField(choices=DocumentType.DOCUMENT_TYPE, default=DocumentType.ANNOTATION)

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

    @property
    def doc_type_str(self):
        if (self.doc_type == DocumentType.ANNOTATION):
            return "Annotation"
        elif (self.doc_type == DocumentType.TRAINING):
            return "Training"
        elif (self.doc_type == DocumentType.TEST):
            return "Test"
        else:
            raise Exception("Unknown document type")

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
        Get a dictionary representation of document for rendering
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
            "project_id": self.project.id,
            "data": self.data,
            "doc_type": self.doc_type_str,
        }

        return doc_out

    def get_doc_annotation_dict(self, json_format="raw", anonymize=True):
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

                if anonymize:
                    annotation_sets[str(annotation.user.id)] = annotation_dict
                else:
                    annotation_sets[annotation.user.username] = annotation_dict

            doc_dict["annotations"] = annotation_sets

        else:
            # Format for JSON in line with GATE formatting
            annotation_sets = {}
            for annotation in annotations:
                a_data = annotation.data
                annotation_set = {
                    "name": annotation.user.id if anonymize else annotation.user.username,
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
    _data = models.JSONField(default=dict)

    @property
    def data(self):
        ann_history = self.latest_annotation_history()
        if ann_history:
            return ann_history.data

        return None

    @data.setter
    def data(self, value):
        # The setter's value actually wraps the input inside a tuple for some reason
        self._append_annotation_history(value)

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

    def change_annotation(self, data, by_user=None, time=timezone.now()):
        if self.status != Annotation.COMPLETED:
            raise RuntimeError("The annotation must be completed before it can be changed")

        self._append_annotation_history(data, by_user, time)

    def _append_annotation_history(self, data, by_user=None, time=timezone.now()):
        if by_user is None:
            by_user = self.user

        AnnotationChangeHistory.objects.create(data=data,
                                               time=time,
                                               annotation=self,
                                               changed_by=by_user)

    def latest_annotation_history(self):
        """
        Convenience function for getting the latest annotation data from the change history.
        Returns None if there's no annotations.
        """
        try:
            last_item = self.change_history.last()
            return last_item
        except models.ObjectDoesNotExist:
            return None

    def get_listing(self):
        """
        Get a dictionary representation of the annotation for rendering.
        """
        output = {
            "id": self.pk,
            "annotated_by": self.user.username,
            "created": self.created,
            "completed": self.status_time if self.status == Annotation.COMPLETED else None,
            "rejected": self.status_time if self.status == Annotation.REJECTED else None,
            "timed_out": self.status_time if self.status == Annotation.TIMED_OUT else None,
            "aborted": self.status_time if self.status == Annotation.ABORTED else None,
            "times_out_at": self.times_out_at,
            "change_list": [change_history.get_listing() for change_history in self.change_history.all()],
        }

        return output

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

    @staticmethod
    def get_annotations_for_user_in_project(user_id, project_id, doc_type=DocumentType.ANNOTATION):
        """
        Gets a list of all completed and pending annotation tasks in the project project_id that belong to the
        annotator with user_id.

        Ordered by descending date and PK so the most recent entry is placed first.
        """

        return Annotation.objects.filter(document__project_id=project_id,
                                         document__doc_type=doc_type,
                                         user_id=user_id).distinct().filter(
            Q(status=Annotation.COMPLETED) | Q(status=Annotation.PENDING)).order_by("-created", "-pk")


class AnnotationChangeHistory(models.Model):
    """
    Model to store the changes in annotation when an annotator makes a change after initial submission
    """
    data = models.JSONField(default=dict)
    time = models.DateTimeField(default=timezone.now)
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name="change_history", null=False)
    changed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="changed_annotations",
                                   null=True)

    def get_listing(self):
        return {
            "id": self.pk,
            "data": self.data,
            "time": self.time,
            "changed_by": self.changed_by.username,
        }
