from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.utils import timezone

from backend.models import Project, Document, Annotation
from backend.utils.serialize import ModelSerializer


class ModelTestCase(TestCase):

    def check_model_field(self, model_class, field_name, field_type):
        self.assertEqual(model_class._meta.get_field(field_name).__class__, field_type)

    def check_model_fields(self, model_class, field_name_types_dict):
        for field_name, field_type in field_name_types_dict.items():
            self.check_model_field(model_class, field_name, field_type)


class TestUserModel(TestCase):

    def test_document_association_check(self):
        user = get_user_model().objects.create(username="test1")
        user2 = get_user_model().objects.create(username="test2")

        project = Project.objects.create()
        doc = Document.objects.create(project=project)
        doc2 = Document.objects.create(project=project)
        user.annotates = project
        user.save()

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


class TestProjectModel(ModelTestCase):

    def setUp(self):
        self.annotations_per_doc = 3
        self.annotator_max_annotation = 0.6
        self.num_docs = 10
        self.num_total_tasks = self.num_docs * self.annotations_per_doc

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
        })

    def check_project_props(self, project, total_tasks, completed_tasks, occupied_tasks, remaining_tasks):
        self.assertEqual(total_tasks, project.num_annotation_tasks_total, "Total tasks check")
        self.assertEqual(completed_tasks, project.num_completed_tasks, "Completed tasks check")
        self.assertTrue(occupied_tasks == project.num_occupied_tasks, "Occupied tasks check")
        self.assertEqual(remaining_tasks, project.num_annotation_tasks_remaining, "Remaining tasks check")

    def test_project_documents(self):
        annotator = get_user_model().objects.create(username="test1")
        project = Project.objects.create(annotations_per_doc=self.annotations_per_doc,
                                         annotator_max_annotation=self.annotator_max_annotation)
        docs = [Document.objects.create(project=project) for i in range(self.num_docs)]

        self.check_project_props(project, total_tasks=self.num_total_tasks,
                                 completed_tasks=0,
                                 occupied_tasks=0,
                                 remaining_tasks=self.num_total_tasks)

        doc = docs[0]
        reject_annotation = Annotation.objects.create(user=annotator, document=doc)
        reject_annotation.reject_annotation()
        self.check_project_props(project, total_tasks=self.num_total_tasks,
                                 completed_tasks=0,
                                 occupied_tasks=0,
                                 remaining_tasks=self.num_total_tasks)

        timeout_annotation = Annotation.objects.create(user=annotator, document=doc)
        timeout_annotation.timeout_annotation()
        self.check_project_props(project, total_tasks=self.num_total_tasks,
                                 completed_tasks=0,
                                 occupied_tasks=0,
                                 remaining_tasks=self.num_total_tasks)

        pending_annotation = Annotation.objects.create(user=annotator, document=doc)
        self.check_project_props(project, total_tasks=self.num_total_tasks,
                                 completed_tasks=0,
                                 occupied_tasks=1,
                                 remaining_tasks=self.num_total_tasks - 1)

        pending_annotation.complete_annotation({})
        self.check_project_props(project, total_tasks=self.num_total_tasks,
                                 completed_tasks=1,
                                 occupied_tasks=1,
                                 remaining_tasks=self.num_total_tasks - 1)

        complete_annotation1 = Annotation.objects.create(user=annotator, document=doc)
        complete_annotation1.complete_annotation({})
        self.check_project_props(project, total_tasks=self.num_total_tasks,
                                 completed_tasks=2,
                                 occupied_tasks=2,
                                 remaining_tasks=self.num_total_tasks - 2)

        complete_annotation2 = Annotation.objects.create(user=annotator, document=docs[1])
        complete_annotation2.complete_annotation({})
        self.check_project_props(project, total_tasks=self.num_total_tasks,
                                 completed_tasks=3,
                                 occupied_tasks=3,
                                 remaining_tasks=self.num_total_tasks - 3)

        complete_annotation3 = Annotation.objects.create(user=annotator, document=docs[2])
        complete_annotation3.complete_annotation({})
        self.check_project_props(project, total_tasks=self.num_total_tasks,
                                 completed_tasks=4,
                                 occupied_tasks=4,
                                 remaining_tasks=self.num_total_tasks - 4)

    def test_project_annotation_timeout(self):
        annotator = get_user_model().objects.create(username="test1")
        project = Project.objects.create(annotations_per_doc=self.annotations_per_doc,
                                         annotator_max_annotation=self.annotator_max_annotation)
        docs = [Document.objects.create(project=project) for i in range(self.num_docs)]
        project.add_annotator(annotator)
        project.save()

        annotation = project.assign_annotator_task(annotator)

        # Check timing out is set properly
        self.assertIsNotNone(annotation)
        self.assertIsNotNone(annotation.times_out_at)

        # Timeout should be more than minutes set in project
        self.assertTrue(annotation.times_out_at > annotation.created)

    def test_saving_and_loading(self):
        name = "Test name"
        created_at = timezone.now()
        data = {
            "entry1": "val1",
            "entry2": "val2"
        }

        proj = Project(name=name, created=created_at, configuration=data)
        proj.save()

        loaded_proj = Project.objects.get(pk=1)
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

        # Load a fresh project model to serialize
        proj = Project.objects.get(pk=1)

        serializer = ModelSerializer()
        serialized_proj = serializer.serialize(proj)

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


class TestAnnotationModel(ModelTestCase):

    def test_model_fields(self):
        self.check_model_fields(Annotation, {
            "user": models.ForeignKey,
            "document": models.ForeignKey,
            "data": models.JSONField,
            "times_out_at": models.DateTimeField,
            "created": models.DateTimeField,
            "status": models.IntegerField,
            "status_time": models.DateTimeField,
        })

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
