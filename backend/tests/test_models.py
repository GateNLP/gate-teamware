import math
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.utils import timezone

from backend.models import Project, Document, DocumentType, Annotation, AnnotatorProject
from backend.utils.serialize import ModelSerializer
# Import signal which is used for cleaning up user pending annotations
import backend.signals


class ModelTestCase(TestCase):

    def check_model_field(self, model_class, field_name, field_type):
        self.assertEqual(model_class._meta.get_field(field_name).__class__, field_type)

    def check_model_fields(self, model_class, field_name_types_dict):
        for field_name, field_type in field_name_types_dict.items():
            self.check_model_field(model_class, field_name, field_type)


class TestUserModel(TestCase):

    def test_agree_privacy_policy(self):
        user = get_user_model().objects.create(username="test1", agreed_privacy_policy=True)
        self.assertTrue(user.agreed_privacy_policy)

    def test_document_association_check(self):
        user = get_user_model().objects.create(username="test1")
        user2 = get_user_model().objects.create(username="test2")

        project = Project.objects.create()
        doc = Document.objects.create(project=project)
        doc2 = Document.objects.create(project=project)
        project.add_annotator(user=user)

        project2 = Project.objects.create()
        doc3 = Document.objects.create(project=project2)

        # Test association where user is an annotator of a project and user2 is not
        self.assertTrue(user.is_associated_with_document(doc))
        self.assertTrue(user.is_associated_with_document(doc2))
        self.assertFalse(user.is_associated_with_document(doc3))

        self.assertFalse(user2.is_associated_with_document(doc))
        self.assertFalse(user2.is_associated_with_document(doc2))
        self.assertFalse(user2.is_associated_with_document(doc3))

        # Same as above but now user and user2 has annotations
        annotation = Annotation.objects.create(user=user, document=doc3)
        annotation2 = Annotation.objects.create(user=user2, document=doc)
        annotation3 = Annotation.objects.create(user=user2, document=doc2)
        annotation4 = Annotation.objects.create(user=user2, document=doc3)

        self.assertTrue(user.is_associated_with_document(doc))
        self.assertTrue(user.is_associated_with_document(doc2))
        self.assertTrue(user.is_associated_with_document(doc3))

        self.assertTrue(user2.is_associated_with_document(doc))
        self.assertTrue(user2.is_associated_with_document(doc2))
        self.assertTrue(user2.is_associated_with_document(doc3))

    def test_check_annotation_association_check(self):
        user = get_user_model().objects.create(username="test1")
        user2 = get_user_model().objects.create(username="test2")
        project = Project.objects.create()
        doc = Document.objects.create(project=project)
        annotation = Annotation.objects.create(user=user, document=doc)

        doc2 = Document.objects.create(project=project)
        annotation2 = Annotation.objects.create(user=user2, document=doc2)

        self.assertTrue(user.is_associated_with_annotation(annotation))
        self.assertFalse(user2.is_associated_with_annotation(annotation))

        self.assertFalse(user.is_associated_with_annotation(annotation2))
        self.assertTrue(user2.is_associated_with_annotation(annotation2))

    def test_check_user_active_project(self):
        user = get_user_model().objects.create(username="test1")
        self.assertFalse(user.has_active_project)
        self.assertEqual(user.active_project, None)

        project = Project.objects.create()
        project.add_annotator(user)
        self.assertTrue(user.has_active_project)
        self.assertEqual(user.active_project, project)

        project.remove_annotator(user)
        self.assertFalse(user.has_active_project)
        self.assertEqual(user.active_project, None)


def create_each_annotation_status_for_user(user: get_user_model(), project: Project):
    annotation_statuses = [Annotation.PENDING,
                           Annotation.COMPLETED,
                           Annotation.REJECTED,
                           Annotation.TIMED_OUT,
                           Annotation.ABORTED]
    for annotation_status in annotation_statuses:
        Annotation.objects.create(user=user,
                                  document=Document.objects.create(project=project),
                                  status=annotation_status)


class TestUserModelDeleteUser(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username="test1",
                                                    first_name="TestFirstname",
                                                    last_name="TestLastname",
                                                    email="test@email.com")
        self.project = Project.objects.create(owner=self.user)
        create_each_annotation_status_for_user(self.user, self.project)

        self.user2 = get_user_model().objects.create(username="test2",
                                                     first_name="TestFirstname",
                                                     last_name="TestLastname",
                                                     email="test2@email.com")
        project2 = Project.objects.create(owner=self.user2)
        Annotation.objects.create(user=self.user,
                                  document=Document.objects.create(project=project2),
                                  status=Annotation.PENDING)
        create_each_annotation_status_for_user(user=self.user2, project=project2)

    def test_clear_pending_annotations(self):
        # Check that there's at least one pending annotation for the user
        self.assertEqual(2, Annotation.objects.filter(status=Annotation.PENDING, user=self.user).count())

        self.user.clear_pending_annotations()

        # No pending annotation for the user
        self.assertEqual(0, Annotation.objects.filter(status=Annotation.PENDING, user=self.user).count())

    def test_remove_user_personal_data(self):
        """
        Tests deleting all personal information of the user from the system and replacing
        all personally identifiable information with placeholders
        """
        self.user.delete_user_personal_information()
        self.user.refresh_from_db()
        TestUserModelDeleteUser.check_user_personal_data_deleted(self, self.user)



    @staticmethod
    def check_user_personal_data_deleted(test_obj, user):
        # Make sure db is refereshed first
        user.refresh_from_db()

        # User should be marked as deleted
        test_obj.assertTrue(user.is_deleted)

        # Deleted username is a combination of [DELETED_USER_USERNAME_PREFIX]_hashedvalues
        test_obj.assertTrue(user.username.startswith(settings.DELETED_USER_USERNAME_PREFIX))
        # Deleted mail is a combination of [DELETED_USER_USERNAME_PREFIX]_hashedvalues@[DELETED_USER_EMAIL_DOMAIN]
        test_obj.assertTrue(user.email.startswith(settings.DELETED_USER_USERNAME_PREFIX))
        test_obj.assertTrue(user.email.endswith(settings.DELETED_USER_EMAIL_DOMAIN))
        # First name and last name should be DELETED_USER_FIRSTNAME and DELETED_USER_LASTNAME
        test_obj.assertEqual(user.first_name, settings.DELETED_USER_FIRSTNAME)
        test_obj.assertEqual(user.last_name, settings.DELETED_USER_LASTNAME)

        # Removed user should not have pending annotations
        test_obj.assertEqual(0, Annotation.objects.filter(status=Annotation.PENDING, user=user).count())

    def test_delete_user(self):
        user_id = self.user.pk
        self.user.delete()
        TestUserModelDeleteUser.check_user_is_deleted(self, user_id)

    @staticmethod
    def check_user_is_deleted(test_obj, user_id):
        test_obj.assertEqual(0, Annotation.objects.filter(user_id=user_id).count(),
                         "Deleted user should not have any annotations")
        test_obj.assertEqual(0, Project.objects.filter(owner_id=user_id).count(),
                         "Deleted user should not have any projects")



class TestDocumentModel(ModelTestCase):

    def test_model_fields(self):
        self.check_model_fields(Document, {
            "project": models.ForeignKey,
            "data": models.JSONField,
            "created": models.DateTimeField,
        })

    def test_document(self):
        annotator = get_user_model().objects.create(username="test1")
        project = Project.objects.create()
        doc = Document.objects.create(project=project)

        # Annotation

        abort_annotation = Annotation.objects.create(user=annotator, document=doc)
        abort_annotation.abort_annotation()
        self.assertFalse(doc.user_completed_annotation_of_document(annotator))

        reject_annotation = Annotation.objects.create(user=annotator, document=doc)
        reject_annotation.reject_annotation()
        self.assertFalse(doc.user_completed_annotation_of_document(annotator))

        timeout_annotation = Annotation.objects.create(user=annotator, document=doc)
        timeout_annotation.timeout_annotation()
        self.assertFalse(doc.user_completed_annotation_of_document(annotator))

        pending_annotation = Annotation.objects.create(user=annotator, document=doc)
        self.assertFalse(doc.user_completed_annotation_of_document(annotator))
        self.assertEqual(1, doc.num_completed_and_pending_annotations)

        complete_annotation1 = Annotation.objects.create(user=annotator, document=doc)
        complete_annotation1.complete_annotation({})
        self.assertTrue(doc.user_completed_annotation_of_document(annotator))
        self.assertEqual(2, doc.num_completed_and_pending_annotations)

        complete_annotation2 = Annotation.objects.create(user=annotator, document=doc)
        complete_annotation2.complete_annotation({})
        complete_annotation3 = Annotation.objects.create(user=annotator, document=doc)
        complete_annotation3.complete_annotation({})

        doc.refresh_from_db()
        self.assertEqual(4, doc.num_completed_and_pending_annotations)
        self.assertEqual(3, doc.num_completed_annotations)
        self.assertEqual(1, doc.num_pending_annotations)
        self.assertEqual(1, doc.num_timed_out_annotations)
        self.assertEqual(1, doc.num_rejected_annotations)
        self.assertEqual(1, doc.num_aborted_annotations)

        self.assertEqual(3, doc.num_user_completed_annotations(annotator))
        self.assertEqual(1, doc.num_user_pending_annotations(annotator))
        self.assertEqual(1, doc.num_user_timed_out_annotations(annotator))
        self.assertEqual(1, doc.num_user_rejected_annotations(annotator))
        self.assertEqual(1, doc.num_user_aborted_annotations(annotator))

    def test_document_type_str(self):
        project = Project.objects.create()
        doc = Document.objects.create(project=project, doc_type=DocumentType.ANNOTATION)
        self.assertEqual("Annotation", doc.doc_type_str)

        doc = Document.objects.create(project=project, doc_type=DocumentType.TRAINING)
        self.assertEqual("Training", doc.doc_type_str)

        doc = Document.objects.create(project=project, doc_type=DocumentType.TEST)
        self.assertEqual("Test", doc.doc_type_str)


class TestProjectModel(ModelTestCase):

    def setUp(self):
        self.annotations_per_doc = 3
        self.annotator_max_annotation = 0.6
        self.num_docs = 10
        self.num_test_docs = 7
        self.num_training_docs = 3
        self.num_annotators = 10
        self.num_total_tasks = self.num_docs * self.annotations_per_doc

        self.project = Project.objects.create(annotations_per_doc=self.annotations_per_doc,
                                              annotator_max_annotation=self.annotator_max_annotation)
        self.docs = [Document.objects.create(project=self.project) for i in range(self.num_docs)]
        self.training_docs = [Document.objects.create(project=self.project, doc_type=DocumentType.TRAINING) for i in
                              range(self.num_training_docs)]
        self.test_docs = [Document.objects.create(project=self.project, doc_type=DocumentType.TEST) for i in
                          range(self.num_test_docs)]

        # Add answers to training docs
        counter = 0
        for doc in self.training_docs:
            doc.data = {
                "id": f"{counter}",
                "text": f"Text{counter}",
                "gold": {
                    "label1": {
                        "value": f"val{counter}",
                        "explanation": f"Exp{counter}"
                    },
                    "label2": {
                        "value": f"val{counter}",
                        "explanation": f"Exp{counter}"
                    },
                }
            }
            doc.save()
            counter += 1

        # Add answers to testing docs
        counter = 0
        for doc in self.test_docs:
            doc.data = {
                "id": f"{counter}",
                "text": f"Text{counter}",
                "gold": {
                    "label1": {
                        "value": f"val{counter}",
                    },
                    "label2": {
                        "value": f"val{counter}",
                    }
                }

            }
            doc.save()
            counter += 1

        self.annotators = [get_user_model().objects.create(username=f"test{i}") for i in range(self.num_annotators)]
        for annotator in self.annotators:
            self.project.add_annotator(annotator)

    def test_model_fields(self):
        self.check_model_fields(Project, {
            "name": models.TextField,
            "description": models.TextField,
            "annotator_guideline": models.TextField,
            "configuration": models.JSONField,
            "owner": models.ForeignKey,
            "annotations_per_doc": models.IntegerField,
            "annotator_max_annotation": models.FloatField,
            "annotation_timeout": models.IntegerField,
            "document_input_preview": models.JSONField,
            "document_id_field": models.TextField,
            "has_training_stage": models.BooleanField,
            "has_test_stage": models.BooleanField,
            "can_annotate_after_passing_training_and_test": models.BooleanField,
            "min_test_pass_threshold": models.FloatField,
            "document_gold_standard_field": models.TextField,

        })

    def test_add_annotator(self):
        project = Project.objects.create()
        annotator = get_user_model().objects.create(username="anno1")
        self.assertEqual(0, project.annotators.all().count())

        project.add_annotator(annotator)
        self.assertEqual(1, project.annotators.all().count())

        annotator_project = AnnotatorProject.objects.get(project=project, annotator=annotator)
        self.assertEqual(AnnotatorProject.ACTIVE, annotator_project.status)

    def test_make_annotator_active(self):
        project = Project.objects.create()
        for i in range(20):
            document = Document.objects.create(project=project)

        project2 = Project.objects.create()
        annotator = get_user_model().objects.create(username="anno1")

        # Fails if not associated with project
        with self.assertRaises(Exception):
            project.make_annotator_active(annotator)

        # Adds to first project and removes
        project.add_annotator(annotator)

        # Fails if already active
        with self.assertRaises(Exception):
            project.make_annotator_active(annotator)

        # Removes from first project and adds to second project
        project.remove_annotator(annotator)
        project2.add_annotator(annotator)

        # Fail if active in another project
        with self.assertRaises(Exception):
            project.make_annotator_active(annotator)

        # Remove from project 2, should now be able to make active in project 1
        project2.remove_annotator(annotator)

        project.make_annotator_active(annotator)
        annotator_project = AnnotatorProject.objects.get(project=project, annotator=annotator)
        self.assertEqual(AnnotatorProject.ACTIVE, annotator_project.status)

        # Adds annotation to project mark user as completed
        for document in project.documents.all():
            annotation = Annotation.objects.create(user=annotator, document=document, status=Annotation.COMPLETED)
        project.remove_annotator(annotator)

        # Fail if already reached quota
        with self.assertRaises(Exception):
            project.make_annotator_active(annotator)

    def test_remove_annotator(self):
        project = Project.objects.create()
        annotator = get_user_model().objects.create(username="anno1")

        project.add_annotator(annotator)
        self.assertEqual(1, project.annotators.all().count())

        project.remove_annotator(annotator)
        self.assertEqual(1, project.annotators.all().count())

        annotator_project = AnnotatorProject.objects.get(project=project, annotator=annotator)
        self.assertEqual(AnnotatorProject.COMPLETED, annotator_project.status)

    def test_reject_annotator(self):
        project = Project.objects.create()
        annotator = get_user_model().objects.create(username="anno1")

        project.add_annotator(annotator)
        self.assertEqual(1, project.annotators.all().count())

        project.reject_annotator(annotator)
        self.assertEqual(1, project.annotators.all().count())

        annotator_project = AnnotatorProject.objects.get(project=project, annotator=annotator)
        self.assertEqual(AnnotatorProject.COMPLETED, annotator_project.status)
        self.assertEqual(True, annotator_project.rejected)

    def test_remove_annotator_clears_pending(self):
        annotator = self.annotators[0]
        # Start a task - should be one pending annotation
        self.project.get_annotator_task(annotator)
        self.assertEqual(1, annotator.annotations.filter(status=Annotation.PENDING).count())

        # remove annotator from project - pending annotations should be cleared
        self.project.remove_annotator(annotator)
        self.assertEqual(0, annotator.annotations.filter(status=Annotation.PENDING).count())

    def test_reject_annotator_clears_pending(self):
        annotator = self.annotators[0]
        # Start a task - should be one pending annotation
        self.project.get_annotator_task(annotator)
        self.assertEqual(1, annotator.annotations.filter(status=Annotation.PENDING).count())

        # reject annotator from project - pending annotations should be cleared
        self.project.reject_annotator(annotator)
        self.assertEqual(0, annotator.annotations.filter(status=Annotation.PENDING).count())

    def test_num_documents(self):
        self.assertEqual(self.project.num_documents, self.num_docs)

    def test_num_test_documents(self):
        self.assertEqual(self.project.num_test_documents, self.num_test_docs)

    def test_num_training_documents(self):
        self.assertEqual(self.project.num_training_documents, self.num_training_docs)

    def test_num_annotation_tasks_total(self):
        self.assertEqual(self.project.num_annotation_tasks_total, self.num_docs * self.annotations_per_doc)

    def test_num_completed_tasks(self):
        self.annotate_docs_all_states(self.docs, self.annotators[0])
        self.annotate_docs_all_states(self.test_docs, self.annotators[0])
        self.annotate_docs_all_states(self.training_docs, self.annotators[0])
        self.assertEqual(self.project.num_completed_tasks, self.num_docs)

    def test_num_pending_tasks(self):
        self.annotate_docs_all_states(self.docs, self.annotators[0])
        self.annotate_docs_all_states(self.test_docs, self.annotators[0])
        self.annotate_docs_all_states(self.training_docs, self.annotators[0])
        self.assertEqual(self.project.num_pending_tasks, self.num_docs)

    def test_num_rejected_tasks(self):
        self.annotate_docs_all_states(self.docs, self.annotators[0])
        self.annotate_docs_all_states(self.test_docs, self.annotators[0])
        self.annotate_docs_all_states(self.training_docs, self.annotators[0])
        self.assertEqual(self.project.num_rejected_tasks, self.num_docs)

    def test_num_timed_out_tasks(self):
        self.annotate_docs_all_states(self.docs, self.annotators[0])
        self.annotate_docs_all_states(self.test_docs, self.annotators[0])
        self.annotate_docs_all_states(self.training_docs, self.annotators[0])
        self.assertEqual(self.project.num_timed_out_tasks, self.num_docs)

    def test_num_aborted_tasks(self):
        self.annotate_docs_all_states(self.docs, self.annotators[0])
        self.annotate_docs_all_states(self.test_docs, self.annotators[0])
        self.annotate_docs_all_states(self.training_docs, self.annotators[0])
        self.assertEqual(self.project.num_aborted_tasks, self.num_docs)

    def test_num_occupied_tasks(self):
        self.annotate_docs_all_states(self.docs, self.annotators[0])
        self.annotate_docs_all_states(self.test_docs, self.annotators[0])
        self.annotate_docs_all_states(self.training_docs, self.annotators[0])
        self.assertEqual(self.project.num_occupied_tasks, self.num_docs * 2,
                         f"Must have {self.num_docs * 2} annotations (completed + pending)")

    def test_num_annotation_tasks_remaining(self):
        self.annotate_docs_all_states(self.docs, self.annotators[0])
        self.annotate_docs_all_states(self.test_docs, self.annotators[0])
        self.annotate_docs_all_states(self.training_docs, self.annotators[0])
        self.assertEqual(self.project.num_annotation_tasks_remaining,
                         self.num_docs * self.annotations_per_doc - self.num_docs * 2)

    def annotate_docs_all_states(self, docs, annotator):
        for doc in docs:
            Annotation.objects.create(user=annotator, document=doc, status=Annotation.REJECTED)
            Annotation.objects.create(user=annotator, document=doc, status=Annotation.COMPLETED)
            Annotation.objects.create(user=annotator, document=doc, status=Annotation.ABORTED)
            Annotation.objects.create(user=annotator, document=doc, status=Annotation.PENDING)
            Annotation.objects.create(user=annotator, document=doc, status=Annotation.TIMED_OUT)

    def test_max_num_task_per_annotator(self):
        self.assertEqual(self.project.max_num_task_per_annotator,
                         math.ceil(self.num_docs * self.annotator_max_annotation))

    def test_num_annotators(self):
        self.assertEqual(self.project.num_annotators, self.num_annotators)

    def test_is_project_configured_and_config_error_message(self):
        # Project has docs but is not configured
        self.assertFalse(self.project.is_project_configured)
        self.assertEqual(len(self.project.project_configuration_error_message), 1)

        # Add a blank configuration with one item
        self.project.configuration = [{}]
        self.project.save()

        # Project is considered configured
        self.assertTrue(self.project.is_project_configured)
        self.assertEqual(len(self.project.project_configuration_error_message), 0)

    def test_project_annotation_timeout(self):
        annotator = self.annotators[0]
        project = self.project
        docs = self.docs

        annotation = project.assign_annotator_task(annotator)

        # Check timing out is set properly
        self.assertIsNotNone(annotation)
        self.assertIsNotNone(annotation.times_out_at)

        # Timeout should be more than minutes set in project
        self.assertTrue(annotation.times_out_at > annotation.created)

    def test_num_annotator_task_remaining(self):

        project = self.project
        docs = self.docs
        annotator = self.annotators[0]
        annotator2 = self.annotators[1]

        num_docs_user_can_annotate = project.max_num_task_per_annotator

        project.refresh_from_db()

        for doc in docs:
            Annotation.objects.create(user=annotator2, document=doc, status=Annotation.COMPLETED)
            Annotation.objects.create(user=annotator2, document=doc, status=Annotation.ABORTED)

        for i in range(math.ceil(
                project.annotator_max_annotation * project.documents.filter(doc_type=DocumentType.ANNOTATION).count())):
            project.refresh_from_db()
            doc = docs[i]
            Annotation.objects.create(user=annotator, document=doc, status=Annotation.COMPLETED)
            Annotation.objects.create(user=annotator, document=doc, status=Annotation.ABORTED)
            self.assertEqual(project.num_annotator_task_remaining(annotator), num_docs_user_can_annotate - (i + 1))
            print(project.num_annotator_task_remaining(annotator))

        self.assertEqual(project.num_annotator_task_remaining(annotator), 0, "Must have 0 tasks remaining")

    def test_get_annotator_annotatable_occupied_completed_pending_documents_query(self):
        project = self.project
        annotator = self.annotators[0]

        # Add some pre-annotated test and training docs to ensure that they do not
        # interfere with actual annotation document counts
        for doc in self.training_docs:
            Annotation.objects.create(document=doc, user=annotator, status=Annotation.COMPLETED)
        for doc in self.test_docs:
            Annotation.objects.create(document=doc, user=annotator, status=Annotation.COMPLETED)

        # Can annotate all docs when blank
        self.assertEqual(project.get_annotator_annotatable_documents_query(annotator).count(), self.num_docs)

        # No annotations so no occupied, completed or pending
        self.assertEqual(project.get_annotator_occupied_documents_query(annotator).count(), 0)
        self.assertEqual(project.get_annotator_completed_documents_query(annotator).count(), 0)
        self.assertEqual(project.get_annotator_pending_documents_query(annotator).count(), 0)

        # One less doc if other annotator has annotated
        for i in range(self.annotations_per_doc):
            ann = self.annotators[i + 1]
            Annotation.objects.create(user=ann, document=self.docs[0], status=Annotation.COMPLETED)

        self.assertEqual(project.get_annotator_annotatable_documents_query(annotator).count(), self.num_docs - 1)

        # Reset annotation state
        Annotation.objects.all().delete()

        # One less doc if other annotator has annotated, should also happen for pending status
        for i in range(self.annotations_per_doc):
            ann = self.annotators[i + 1]
            Annotation.objects.create(user=ann, document=self.docs[0], status=Annotation.PENDING)

        self.assertEqual(project.get_annotator_annotatable_documents_query(annotator).count(), self.num_docs - 1)

        # Rejected
        Annotation.objects.create(user=annotator, document=self.docs[1], status=Annotation.REJECTED)
        self.assertEqual(project.get_annotator_annotatable_documents_query(annotator).count(), self.num_docs - 2)
        self.assertEqual(project.get_annotator_occupied_documents_query(annotator).count(), 1)
        self.assertEqual(project.get_annotator_completed_documents_query(annotator).count(), 0)
        self.assertEqual(project.get_annotator_pending_documents_query(annotator).count(), 0)

        # Pending
        Annotation.objects.create(user=annotator, document=self.docs[2], status=Annotation.PENDING)
        self.assertEqual(project.get_annotator_annotatable_documents_query(annotator).count(), self.num_docs - 3)
        self.assertEqual(project.get_annotator_occupied_documents_query(annotator).count(), 2)
        self.assertEqual(project.get_annotator_completed_documents_query(annotator).count(), 0)
        self.assertEqual(project.get_annotator_pending_documents_query(annotator).count(), 1)

        # Completed
        Annotation.objects.create(user=annotator, document=self.docs[3], status=Annotation.COMPLETED)
        self.assertEqual(project.get_annotator_annotatable_documents_query(annotator).count(), self.num_docs - 4)
        self.assertEqual(project.get_annotator_occupied_documents_query(annotator).count(), 3)
        self.assertEqual(project.get_annotator_completed_documents_query(annotator).count(), 1)
        self.assertEqual(project.get_annotator_pending_documents_query(annotator).count(), 1)

        # Aborted should not affect count
        Annotation.objects.create(user=annotator, document=self.docs[3], status=Annotation.ABORTED)
        self.assertEqual(project.get_annotator_annotatable_documents_query(annotator).count(), self.num_docs - 4)
        self.assertEqual(project.get_annotator_occupied_documents_query(annotator).count(), 3)
        self.assertEqual(project.get_annotator_completed_documents_query(annotator).count(), 1)
        self.assertEqual(project.get_annotator_pending_documents_query(annotator).count(), 1)

        # Timed out should not affect count
        Annotation.objects.create(user=annotator, document=self.docs[3], status=Annotation.TIMED_OUT)
        self.assertEqual(project.get_annotator_annotatable_documents_query(annotator).count(), self.num_docs - 4)
        self.assertEqual(project.get_annotator_occupied_documents_query(annotator).count(), 3)
        self.assertEqual(project.get_annotator_completed_documents_query(annotator).count(), 1)
        self.assertEqual(project.get_annotator_pending_documents_query(annotator).count(), 1)

    def test_annotator_reached_quota(self):
        num_tasks_to_complete = math.ceil(self.num_docs * self.annotator_max_annotation)
        annotator = self.annotators[0]

        for i in range(num_tasks_to_complete):
            self.assertFalse(self.project.annotator_reached_quota(annotator))
            Annotation.objects.create(user=annotator, document=self.docs[i], status=Annotation.COMPLETED)

        self.assertTrue(self.project.annotator_reached_quota(annotator))

    def test_annotator_completed_training(self):
        annotator = self.annotators[0]
        self.project.annotator_completed_training(annotator)

        annotator_proj = AnnotatorProject.objects.get(annotator=annotator, project=self.project)
        self.assertTrue(annotator_proj.training_completed is not None)
        self.assertTrue(annotator_proj.training_score == 0)

    def test_annotator_completed_test(self):
        annotator = self.annotators[0]
        self.project.annotator_completed_test(annotator)

        annotator_proj = AnnotatorProject.objects.get(annotator=annotator, project=self.project)
        self.assertTrue(annotator_proj.test_completed is not None)
        self.assertTrue(annotator_proj.test_score == 0)

    def test_annotator_set_allowed_to_annotate(self):
        annotator = self.annotators[0]
        self.project.annotator_set_allowed_to_annotate(annotator)

        annotator_proj = AnnotatorProject.objects.get(annotator=annotator, project=self.project)
        self.assertTrue(annotator_proj.allowed_to_annotate is True)

    def test_annotator_completed_annotation(self):
        annotator = self.annotators[0]
        self.project.remove_annotator(annotator)

        annotator_proj = AnnotatorProject.objects.get(annotator=annotator, project=self.project)
        self.assertTrue(annotator_proj.status == AnnotatorProject.COMPLETED)

    def test_get_annotator_document_score(self):
        annotator = self.annotators[0]
        # No annotations == 0
        self.assertEqual(0, self.project.get_annotator_document_score(annotator, DocumentType.TEST))

        incorrect_data = {
            "label1": "Incorrect",
            "label2": "Incorrect"
        }

        # All incorrect
        for doc in self.test_docs:
            anno = Annotation.objects.create(user=annotator, document=doc, status=Annotation.COMPLETED)
            anno.data = incorrect_data

        self.assertEqual(0, self.project.get_annotator_document_score(annotator, DocumentType.TEST))

        # All correct
        annotator2 = self.annotators[1]
        for doc in self.test_docs:
            correct_annotation_data = {
                "label1": doc.data["gold"]["label1"]["value"],
                "label2": doc.data["gold"]["label2"]["value"],
            }
            anno = Annotation.objects.create(user=annotator2, document=doc, status=Annotation.COMPLETED)
            anno.data = correct_annotation_data

        self.assertEqual(self.num_test_docs, self.project.get_annotator_document_score(annotator2, DocumentType.TEST))

        # 4 correct
        num_correct = 4
        annotator3 = self.annotators[2]
        counter = 0
        for doc in self.test_docs:
            correct_annotation_data = {
                "label1": doc.data["gold"]["label1"]["value"],
                "label2": doc.data["gold"]["label2"]["value"],
            }
            data = correct_annotation_data if counter < num_correct else incorrect_data
            anno = Annotation.objects.create(user=annotator3, document=doc, status=Annotation.COMPLETED)
            anno.data = data
            counter += 1

        self.assertEqual(num_correct, self.project.get_annotator_document_score(annotator3, DocumentType.TEST))

    def test_check_annotation_answer(self):

        # Label with single string value
        answers_str_label = {
            "label1": {
                "value": "answer"
            }
        }
        annotation_str_label = {
            "label1": "answer"
        }

        # Correct str answer
        self.assertTrue(self.project.check_annotation_answer(annotation_str_label, answers_str_label))

        # Incorrect str answer
        annotation_str_label["label1"] = "Incorrect"
        self.assertFalse(self.project.check_annotation_answer(annotation_str_label, answers_str_label))

        # Label with list value (multiple choice)
        answers_list_label = {
            "label1": {
                "value": ["answer1", "answer3", "answer2"]
            }
        }
        annotation_list_label = {
            "label1": ["answer2", "answer1", "answer3"]
        }
        self.assertTrue(self.project.check_annotation_answer(annotation_list_label, answers_list_label))

        # One wrong value
        annotation_list_label["label1"] = ["answer2", "answer1", "answer4"]
        self.assertFalse(self.project.check_annotation_answer(annotation_list_label, answers_list_label))

        # Too many values
        annotation_list_label["label1"] = ["answer2", "answer1", "answer3", "answer4"]
        self.assertFalse(self.project.check_annotation_answer(annotation_list_label, answers_list_label))

        # Missing a value
        annotation_list_label["label1"] = ["answer2", "answer3"]
        self.assertFalse(self.project.check_annotation_answer(annotation_list_label, answers_list_label))

        # Two labels with str and list
        answers_list_str_label = {
            "label1": {
                "value": ["answer1", "answer3", "answer2"]
            },
            "label2": {
                "value": "answer"
            }
        }
        annotation_list_str_label = {
            "label1": ["answer2", "answer1", "answer3"],
            "label2": "answer",
        }
        self.assertTrue(self.project.check_annotation_answer(annotation_list_str_label, answers_list_str_label))

        # Has additional label in annotation, is ok and won't be included in the check
        annotation_list_str_label["label3"] = "Other answer"
        self.assertTrue(self.project.check_annotation_answer(annotation_list_str_label, answers_list_str_label))

        # Missing one label in annotation
        annotation_list_str_label.pop("label2")
        self.assertFalse(self.project.check_annotation_answer(annotation_list_str_label, answers_list_str_label))

    def test_saving_and_loading(self):
        name = "Test name"
        created_at = timezone.now()
        data = {
            "entry1": "val1",
            "entry2": "val2"
        }

        proj = Project(name=name, created=created_at, configuration=data)
        proj.save()

        loaded_proj = Project.objects.get(pk=proj.pk)
        self.assertEqual(loaded_proj.name, name)
        self.assertEqual(loaded_proj.created, created_at)
        proj_data = loaded_proj.configuration
        self.assertEqual(proj_data["entry1"], data["entry1"])
        self.assertEqual(proj_data["entry2"], data["entry2"])

    def test_serializing(self):
        user1 = get_user_model().objects.create(username="user1")
        user2 = get_user_model().objects.create(username="user2")

        name = "Test name"
        created_at = timezone.now()
        data = {
            "entry1": "val1",
            "entry2": "val2"
        }
        proj = Project(name=name, created=created_at, configuration=data)
        proj.save()

        # One document
        document = Document.objects.create(project=proj)
        document.project = proj
        document.save()

        # Two document
        document2 = Document.objects.create(project=proj)

        # User 1 as owner
        user1.owns.add(proj)
        user1.save()

        # Refresh project model and serialize
        proj.refresh_from_db()

        serializer = ModelSerializer()
        serialized_proj = serializer.serialize(proj, exclude_fields=set(["annotatorproject"]))

        self.assertEqual(serialized_proj["name"], proj.name)
        self.assertEqual(serialized_proj["configuration"], proj.configuration)
        self.assertEqual(serialized_proj["owner"], user1.id)
        self.assertEqual(serialized_proj["documents"], [document.id, document2.id])

    def test_deserialize(self):
        name = "Test name"
        created_at = timezone.now()
        data = {
            "entry1": "val1",
            "entry2": "val2"
        }

        user1 = get_user_model().objects.create(username="user1")
        user2 = get_user_model().objects.create(username="user2")
        proj = Project()
        proj.save()

        input_dict = {
            "id": proj.id,
            "name": name,
            "created_at": created_at,
            "data": data,
            "owner": user1.id
        }

        serializer = ModelSerializer()
        deserialized_obj = serializer.deserialize(Project, input_dict)

        self.assertEqual(input_dict["name"], deserialized_obj.name)
        self.assertEqual(input_dict["owner"], deserialized_obj.owner.id)

    def test_clone_project(self):

        project_fields = {
            "description",
            "annotator_guideline",
            "configuration",
            "annotations_per_doc",
            "annotator_max_annotation",
            "allow_document_reject",
            "allow_annotation_change",
            "annotation_timeout",
            "document_input_preview",
            "document_input_preview_csv",
            "document_id_field",
            "has_training_stage",
            "has_test_stage",
            "can_annotate_after_passing_training_and_test",
            "min_test_pass_threshold",
            "document_gold_standard_field",
            "document_pre_annotation_field",
        }

        clone_prefix = "Test project prefix "

        # Check fields must match exactly
        fields = Project.get_project_config_fields({"name", "owner", "id", "created", "uuid"})
        field_name_set = set()
        for field in fields:
            field_name_set.add(field.name)

        self.assertSetEqual(project_fields, field_name_set)

        project = Project.objects.create(name="Testname",
                                         description="Test desc",
                                         annotator_guideline="Test annotator guideline",
                                         configuration=[
                                             {
                                                 "name": "sentiment",
                                                 "title": "Sentiment",
                                                 "type": "radio",
                                                 "options": {
                                                     "positive": "Positive",
                                                     "negative": "Negative",
                                                     "neutral": "Neutral"
                                                 }
                                             },
                                             {
                                                 "name": "reason",
                                                 "title": "Reason for your stated sentiment",
                                                 "type": "textarea"
                                             }
                                         ],
                                         annotations_per_doc=3,
                                         annotator_max_annotation=0.3,
                                         allow_document_reject=False,
                                         allow_annotation_change=False,
                                         annotation_timeout=809,
                                         document_input_preview={"test": "testest"},
                                         document_id_field="test_field_name",
                                         has_training_stage=False,
                                         has_test_stage=False,
                                         can_annotate_after_passing_training_and_test=False,
                                         min_test_pass_threshold=0.9,
                                         document_gold_standard_field="test_fname",
                                         )
        cloned_project = project.clone(clone_name_prefix=clone_prefix)
        # Check ID and name
        self.assertNotEqual(project.id, cloned_project.id)
        self.assertEqual(clone_prefix + project.name, cloned_project.name)
        # Check cloned parameters
        for field_name in project_fields:
            self.assertEqual(getattr(project, field_name), getattr(cloned_project, field_name))


class TestAnnotationModel(ModelTestCase):

    def test_model_fields(self):
        self.check_model_fields(Annotation, {
            "user": models.ForeignKey,
            "document": models.ForeignKey,
            "times_out_at": models.DateTimeField,
            "created": models.DateTimeField,
            "status": models.IntegerField,
            "status_time": models.DateTimeField,
        })

    def test_model_data(self):
        """Getting and setting data to the annotation model"""

        project = Project.objects.create(name="Test")
        document = Document.objects.create(project=project)
        user = get_user_model().objects.create(username="test1")
        annotation = Annotation.objects.create(document=document, user=user)

        annotation_test_data = {
            "id": 10,
            "label": "Test annotation content"
        }

        annotation_test_data_changed = {
            "id": 50,
            "label": "Test annotation content 2"
        }

        annotation.data = annotation_test_data
        self.assertDictEqual(annotation_test_data, annotation.data, "Contents of returned dict should be the same")

        annotation.data = annotation_test_data_changed
        self.assertDictEqual(annotation_test_data_changed, annotation.data,
                             "Contents of returned dict should be the same")

        anno_db_fetch = Annotation.objects.get(pk=annotation.id)
        self.assertDictEqual(annotation_test_data_changed, anno_db_fetch.data,
                             "Contents of returned dict should be the smae")

    def test_timeout_check(self):
        num_already_timedout = 12
        num_completed = 50
        num_rejected = 4
        num_to_timeout = 23
        current_time = timezone.now()
        timeout_time = current_time + timedelta(minutes=30)
        timeout_check_time = current_time + timedelta(minutes=31)

        annotator = get_user_model().objects.create(username="test1")
        project = Project.objects.create()
        document = Document.objects.create(project=project)

        for i in range(num_already_timedout):
            Annotation.objects.create(document=document,
                                      user=annotator,
                                      times_out_at=timeout_time,
                                      status=Annotation.TIMED_OUT,
                                      status_time=timeout_time)

        for i in range(num_completed):
            Annotation.objects.create(document=document,
                                      user=annotator,
                                      times_out_at=timeout_time,
                                      status=Annotation.COMPLETED,
                                      status_time=timeout_time)

        for i in range(num_rejected):
            Annotation.objects.create(document=document,
                                      user=annotator,
                                      times_out_at=timeout_time,
                                      status=Annotation.REJECTED,
                                      status_time=timeout_time)

        for i in range(num_to_timeout):
            Annotation.objects.create(document=document,
                                      user=annotator,
                                      times_out_at=timeout_time)

        self.assertEqual(num_already_timedout + num_completed + num_rejected + num_to_timeout,
                         Annotation.objects.all().count(), "Must have this many number of annotations in total")

        num_timed_out = Annotation.check_for_timed_out_annotations(current_time + timedelta(minutes=15))
        self.assertEqual(0, num_timed_out, "There should be no timed out annotations yet")

        num_timed_out = Annotation.check_for_timed_out_annotations(timeout_check_time)
        self.assertEqual(num_to_timeout, num_timed_out, "Number of timed annotations to timeout must be equal")

        num_timed_out = Annotation.check_for_timed_out_annotations(timeout_check_time + timedelta(hours=1))
        self.assertEqual(0, num_timed_out, "Must not be anymore annotations to timeout")

    def test_change_annotation(self):

        original_annotation = {"label1": "value1"}
        changed_annotation = {"label1": "value2"}
        changed_annotation2 = {"label1": "value3"}

        project = Project.objects.create()
        document = Document.objects.create(project=project)
        annotator = get_user_model().objects.create(username="Testannotator")
        annotator2 = get_user_model().objects.create(username="Testannotator2")
        annotation = Annotation.objects.create(document=document, user=annotator)

        with self.assertRaises(RuntimeError):
            # Error should be raised if annotation not already completed
            annotation.change_annotation(changed_annotation, annotator2)

        # Complete the annotation
        annotation.complete_annotation(original_annotation)
        self.assertDictEqual(original_annotation, annotation.data, "Expects the original annotation")

        # Change the annotation by setting the data property
        annotation.data = changed_annotation
        annotation.refresh_from_db()

        self.assertDictEqual(changed_annotation, annotation.data, "Expects the first annotation change")
        self.assertEqual(annotator,
                         annotation.latest_annotation_history().changed_by,
                         "Changed by the owner of the annotation object by default")

        # Change the annotation using change_annotation method
        annotation.change_annotation(changed_annotation2, annotator2)
        self.assertDictEqual(changed_annotation2, annotation.data, "Expects the second annotation change")
        self.assertEqual(annotator2,
                         annotation.latest_annotation_history().changed_by,
                         "Should be changed by annotator2")

    def test_get_annotations_for_user_in_project(self):
        num_projects = 3
        num_annotators = 4
        num_annotations_for_annotator = 4

        projects = [Project.objects.create() for i in range(num_projects)]
        annotators = [get_user_model().objects.create(username=f"Testannotator{i}") for i in range(num_annotators)]
        doc_types = [DocumentType.ANNOTATION, DocumentType.TRAINING, DocumentType.TEST]
        anno_status = [Annotation.PENDING, Annotation.COMPLETED,
                       Annotation.REJECTED, Annotation.ABORTED, Annotation.TIMED_OUT]

        # Create annotations for all annotators
        for project in projects:
            for annotator in annotators:
                for i in range(num_annotations_for_annotator):
                    for doc_type in doc_types:
                        for status in anno_status:
                            doc = Document.objects.create(project=project, doc_type=doc_type)
                            Annotation.objects.create(user=annotator, document=doc, status=status)

        # Check for all annotators and projects
        for project in projects:
            for annotator in annotators:
                # Shows 4 pending and 4 completed annotations
                self.assertEqual(num_annotations_for_annotator * 2,
                                 len(Annotation.get_annotations_for_user_in_project(annotator.pk, project.pk)))
                self.assertEqual(num_annotations_for_annotator * 2,
                                 len(Annotation.get_annotations_for_user_in_project(annotator.pk,
                                                                                    project.pk,
                                                                                    DocumentType.TEST)))
                self.assertEqual(num_annotations_for_annotator * 2,
                                 len(Annotation.get_annotations_for_user_in_project(annotator.pk,
                                                                                    project.pk,
                                                                                    DocumentType.TRAINING)))


class TestDocumentAnnotationModelExport(TestCase):

    def setUp(self):
        self.unanonymized_prefix = "namedperson"
        self.test_user = get_user_model().objects.create(username="project_creator")
        self.annotator_names = [f"{self.unanonymized_prefix}{i}" for i in range(3)]
        self.annotators = [get_user_model().objects.create(username=u) for u in self.annotator_names]
        self.anon_annotator_names = [f"{settings.ANONYMIZATION_PREFIX}{a.id}" for a in self.annotators]
        self.project = Project.objects.create(owner=self.test_user)
        for i in range(10):
            document = Document.objects.create(
                project=self.project,
                data={
                    "id": i,
                    "text": f"Text {i}",
                    "feature1": "Testvalue 1",
                    "feature2": "Testvalue 1",
                    "feature3": "Testvalue 1",
                    "features": {
                        "gate_format_feature1": "Gate feature test value",
                        "gate_format_feature2": "Gate feature test value",
                        "gate_format_feature3": "Gate feature test value",
                    },
                    "offset_type": "x",
                    "annotations": {
                        "existing_annotator1": {
                            "sentiment": "positive"
                        },
                        f"{settings.ANONYMIZATION_PREFIX}{self.annotators[0].pk}": {
                            "sentiment": "positive"
                        }

                    },
                    "annotation_sets": {
                        "existing_annotator1": {
                            "name": "existing_annotator1",
                            "annotations": [
                                {
                                    "type": "Document",
                                    "start": 0,
                                    "end": 10,
                                    "id": 0,
                                    "features": {
                                        "sentiment": "positive"
                                    }
                                }
                            ],
                            "next_annid": 1
                        },
                        f"{settings.ANONYMIZATION_PREFIX}{self.annotators[0].pk}": {
                            "name": f"{settings.ANONYMIZATION_PREFIX}{self.annotators[0].pk}",
                            "annotations": [
                                {
                                    "type": "Document",
                                    "start": 0,
                                    "end": 10,
                                    "id": 0,
                                    "features": {
                                        "sentiment": "positive"
                                    }
                                }
                            ],
                            "next_annid": 1
                        }

                    }


                }
            )

            for annotator in self.annotators:
                annotation = Annotation.objects.create(user=annotator,
                                                       document=document,
                                                       status=Annotation.COMPLETED,
                                                       )
                annotation.data = {
                    "text1": "Value1",
                    "checkbox1": ["val1", "val2", "val3"],
                }

                annotation_pending = Annotation.objects.create(user=annotator,
                                                               document=document,
                                                               status=Annotation.PENDING)

                annotation_timed_out = Annotation.objects.create(user=annotator,
                                                                 document=document,
                                                                 status=Annotation.TIMED_OUT)

                annotation_reject = Annotation.objects.create(user=annotator,
                                                              document=document,
                                                              status=Annotation.REJECTED)

                annotation_aborted = Annotation.objects.create(user=annotator,
                                                               document=document,
                                                               status=Annotation.ABORTED)

        self.project.refresh_from_db()

    def test_export_raw(self):

        for document in self.project.documents.all():
            # Fields should remain exactly the same as what's been uploaded
            # aside from  annotation_sets
            doc_dict = document.get_doc_annotation_dict("raw")
            print(doc_dict)
            self.assertTrue("id" in doc_dict)
            self.assertTrue("text" in doc_dict)
            self.assertTrue("feature1" in doc_dict)
            self.assertTrue("feature2" in doc_dict)
            self.assertTrue("feature3" in doc_dict)
            self.assertTrue("features" in doc_dict)
            self.assertTrue("offset_type" in doc_dict)
            self.assertTrue("annotations" in doc_dict)
            doc_features = doc_dict["features"]
            self.assertTrue("gate_format_feature1" in doc_features)
            self.assertTrue("gate_format_feature2" in doc_features)
            self.assertTrue("gate_format_feature3" in doc_features)


            self.check_raw_gate_annotation_formatting(doc_dict)
            self.check_teamware_status(doc_dict, self.anon_annotator_names)

    def test_export_gate(self):

        for document in self.project.documents.all():
            # All top-level fields apart from name, text, features and annotation_sets should be
            # nested inside the features field
            doc_dict = document.get_doc_annotation_dict("gate")
            print(doc_dict)

            self.assertTrue("text" in doc_dict)
            self.assertTrue("features" in doc_dict)
            self.assertFalse("annotations" in doc_dict)
            self.assertEqual(doc_dict["offset_type"], "x")
            doc_features = doc_dict["features"]
            self.assertTrue("id" in doc_features)
            self.assertTrue("feature1" in doc_features)
            self.assertTrue("feature2" in doc_features)
            self.assertTrue("feature3" in doc_features)
            self.assertTrue("annotations" in doc_features)
            self.assertFalse("features" in doc_features, "Double nesting of features field")
            self.assertFalse("offset_type" in doc_features, "Double nesting of offset_type field")
            self.assertTrue("gate_format_feature1" in doc_features)
            self.assertTrue("gate_format_feature2" in doc_features)
            self.assertTrue("gate_format_feature3" in doc_features)

            self.check_raw_gate_annotation_formatting(doc_dict)
            self.check_teamware_status(doc_features, self.anon_annotator_names)

    def test_export_gate_with_no_offset_type(self):

        for document in self.project.documents.all():
            document.data.pop("offset_type")

            doc_dict = document.get_doc_annotation_dict("gate")
            self.assertEqual(doc_dict["offset_type"], "p", "offset_type should default to p")


    def check_raw_gate_annotation_formatting(self, doc_dict: dict):
        self.assertTrue("annotation_sets" in doc_dict)
        self.assertEqual(len(doc_dict["annotation_sets"]), 4, doc_dict)

        # Test annotation formatting
        for aset_key, aset_data in doc_dict["annotation_sets"].items():
            if aset_key != "existing_annotator1":
                self.assertTrue("name" in aset_data)
                self.assertTrue("annotations" in aset_data)
                self.assertEqual(len(aset_data["annotations"]), 1)
                anno_dict = aset_data["annotations"][0]
                self.assertTrue("type" in anno_dict)
                self.assertTrue("start" in anno_dict)
                self.assertTrue("end" in anno_dict)
                self.assertTrue("id" in anno_dict)
                self.assertTrue("features" in anno_dict)
                features_dict = anno_dict["features"]
                self.assertTrue("text1" in features_dict)
                self.assertTrue("checkbox1" in features_dict)
            else:
                # Check that existing annotation from document upload is carried over
                self.assertEqual(aset_data["annotations"][0]["features"]["sentiment"], "positive")




    def check_teamware_status(self, containing_dict, expected_value):
        self.assertTrue("teamware_status" in containing_dict)
        teamware_status = containing_dict["teamware_status"]
        if isinstance(expected_value, str):
            self.assertEqual(teamware_status["rejected_by"], expected_value)
            self.assertEqual(teamware_status["aborted"], expected_value)
            self.assertEqual(teamware_status["timed_out"], expected_value)
        else:
            self.assertSetEqual(set(teamware_status["rejected_by"]), set(expected_value))
            self.assertSetEqual(set(teamware_status["aborted"]), set(expected_value))
            self.assertSetEqual(set(teamware_status["timed_out"]), set(expected_value))

    def test_export_csv(self):

        for document in self.project.documents.all():
            doc_dict = document.get_doc_annotation_dict("csv")
            print(doc_dict)

            self.assertTrue("id" in doc_dict)
            self.assertTrue("text" in doc_dict)
            self.assertTrue("feature1" in doc_dict)
            self.assertTrue("feature2" in doc_dict)
            self.assertTrue("feature3" in doc_dict)
            self.assertTrue("annotations" in doc_dict)
            self.assertEqual(len(doc_dict["annotations"]), 4, doc_dict)
            anno_set_dict = doc_dict["annotations"]
            for set_key in anno_set_dict:
                if set_key != "existing_annotator1":
                    self.assertTrue(isinstance(anno_set_dict[set_key]["text1"], str))
                    self.assertTrue(isinstance(anno_set_dict[set_key]["checkbox1"], str))
                else:
                    self.assertEqual(anno_set_dict[set_key]["sentiment"], "positive")

            self.check_teamware_status(doc_dict, ",".join(str(i) for i in self.anon_annotator_names))

    def test_export_raw_anonymized(self):

        for document in self.project.documents.all():
            # Mask any existing annotations that came with the document upload
            document.data.pop("annotation_sets")
            document.save()

            doc_dict = document.get_doc_annotation_dict("raw", anonymize=True)

            for aset_key, aset_data in doc_dict["annotation_sets"].items():
                self.assertFalse(aset_key.startswith(self.unanonymized_prefix))
                self.assertFalse(aset_data.get("name", None).startswith(self.unanonymized_prefix))

            self.check_teamware_status(doc_dict, self.anon_annotator_names)

    def test_export_raw_deanonymized(self):

        for document in self.project.documents.all():
            # Mask any existing annotations that came with the document upload
            document.data.pop("annotation_sets")
            document.save()

            doc_dict = document.get_doc_annotation_dict("raw", anonymize=False)

            for aset_key, aset_data in doc_dict["annotation_sets"].items():
                self.assertTrue(aset_key.startswith(self.unanonymized_prefix))
                self.assertTrue(aset_data.get("name", None).startswith(self.unanonymized_prefix))

            # for non-anonymized export the rejected/aborted/timed_out status
            # uses names rather than ID numbers
            self.check_teamware_status(doc_dict, self.annotator_names)

    def test_export_gate_anonymized(self):

        for document in self.project.documents.all():
            # Mask any existing annotations that came with the document upload
            document.data.pop("annotation_sets")
            document.save()

            doc_dict = document.get_doc_annotation_dict("gate", anonymize=True)

            for aset_key, aset_data in doc_dict["annotation_sets"].items():
                self.assertFalse(aset_key.startswith(self.unanonymized_prefix))
                self.assertFalse(aset_data.get("name", None).startswith(self.unanonymized_prefix))

            self.check_teamware_status(doc_dict["features"], self.anon_annotator_names)

    def test_export_gate_deanonymized(self):

        for document in self.project.documents.all():
            # Mask any existing annotations that came with the document upload
            document.data.pop("annotation_sets")
            document.save()

            doc_dict = document.get_doc_annotation_dict("gate", anonymize=False)

            for aset_key, aset_data in doc_dict["annotation_sets"].items():
                self.assertTrue(aset_key.startswith(self.unanonymized_prefix))
                self.assertTrue(aset_data.get("name", None).startswith(self.unanonymized_prefix))

            # for non-anonymized export the rejected/aborted/timed_out status
            # uses names rather than ID numbers
            self.check_teamware_status(doc_dict["features"], self.annotator_names)
