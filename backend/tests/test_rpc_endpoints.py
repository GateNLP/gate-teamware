from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.utils import timezone
import json

from backend.models import Annotation, Document, Project
from backend.rpc import create_project, update_project, add_project_document, add_document_annotation, \
    get_possible_annotators, add_project_annotator, remove_project_annotator, get_project_annotators, \
    get_annotation_task, complete_annotation_task, reject_annotation_task
from backend.rpcserver import rpc_method


@rpc_method
def rpc_endpoint_for_test_call(request, a, b):
    return a + b


class TestEndpoint(TestCase):
    username = "testuser"
    password = "123456789"
    user_email = "test@test.com"

    factory = RequestFactory()

    user = None
    client = None

    def get_default_user(self):

        if not self.user:
            self.user = get_user_model().objects.create(username=self.username)
            self.user.set_password(self.password)
            self.user.save()

        return self.user

    def get_request(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        return request

    def get_loggedin_request(self):
        request = self.factory.get("/")
        request.user = self.get_default_user()
        return request

    def get_client(self):
        if not self.client:
            self.client = Client()
        return self.client

    def get_loggedin_client(self):
        client = self.get_client()
        user = self.get_default_user()
        self.assertTrue(client.login(username=self.username, password=self.password))
        return client

    def call_rpc(self, client, method_name, *params):
        response = client.post("/rpc/", {
            "jsonrpc": "2.0",
            "id": 0,
            "method": method_name,
            "params": list(params)
        }, content_type="application/json")
        return response


class TestTestEndpoint(TestCase):
    def test_call_rpc(self):
        e = TestEndpoint()
        c = e.get_client()
        response = e.call_rpc(c, "rpc_endpoint_for_test_call", 2, 3)
        self.assertEqual(response.status_code, 200)
        msg = json.loads(response.content)
        self.assertEqual(msg["result"], 5)

    def test_client_loggedin(self):
        e = TestEndpoint()
        self.assertIsNotNone(e.get_loggedin_client())


class TestUserAuth(TestCase):

    def test_user_auth(self):
        username = "testuser"
        user_pass = "123456789"
        user_email = "test@test.com"

        c = Client()

        # Register
        params = {
            "username": username,
            "password": user_pass,
            "email": user_email,
        }
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "register", "id": 20, "params": [params]},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        msg = json.loads(response.content)
        self.assertEqual(msg["result"]["isAuthenticated"], True)

        # Log in
        params = {
            "username": username,
            "password": user_pass,
        }
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "login", "id": 20, "params": [params]},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        msg = json.loads(response.content)
        self.assertEqual(msg["result"]["isAuthenticated"], True)

        # Check authentication
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "is_authenticated", "id": 20},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        msg = json.loads(response.content)
        self.assertEqual(msg["result"]["isAuthenticated"], True)

        # Log Out
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "logout", "id": 20},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)


class TestProject(TestEndpoint):

    def test_create_project(self):
        proj_obj = create_project(self.get_loggedin_request())
        self.assertIsNotNone(proj_obj)
        self.assertTrue('id' in proj_obj)
        self.assertTrue(proj_obj['id'] > 0)
        self.assertTrue('name' in proj_obj)

        saved_proj = Project.objects.get(pk=proj_obj['id'])
        self.assertEqual(saved_proj.owner.pk, self.get_default_user().pk)  # Owner is project creator

    def test_update_project(self):
        project = Project.objects.create()

        data = {
            "id": project.pk,
            "name": "Test project",
            "configuration": [
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
        }

        self.assertTrue(update_project(self.get_loggedin_request(), data))

        saved_proj = Project.objects.get(pk=project.pk)
        self.assertEqual(len(saved_proj.configuration), 2)


class TestDocument(TestEndpoint):

    def test_create_document(self):
        proj = Project.objects.create(owner=self.get_default_user())
        test_doc = {
            "text": "Test text"
        }
        doc_id = add_project_document(self.get_loggedin_request(), proj.pk, test_doc)
        self.assertTrue(doc_id > 0)

        doc = Document.objects.get(pk=doc_id)
        self.assertEqual(doc.project.pk, proj.pk)
        self.assertEqual(doc.data["text"], "Test text")  # Data check


class TestAnnotation(TestEndpoint):

    def test_add_annotation(self):
        proj = Project.objects.create(owner=self.get_default_user())
        doc = Document.objects.create(project=proj)

        test_annote = {
            "label1": "value1"
        }

        annote_id = add_document_annotation(self.get_loggedin_request(), doc.pk, test_annote)

        annotation = Annotation.objects.get(pk=annote_id)
        self.assertEqual(annotation.user.pk, self.get_default_user().pk)  # Annotation linked to user
        self.assertEqual(annotation.data["label1"], "value1")  # Data check


class TestAnnotationExport(TestEndpoint):

    def test_rpc_get_annotations_endpoint(self):
        user = self.get_default_user()
        c = self.get_loggedin_client()

        ##setup
        project = Project.objects.create()

        with open('examples/documents.json') as f:
            for input_document in json.load(f):
                document = Document.objects.create(project=project, data=input_document)
                Annotation.objects.create(user=user, document=document, data={"testannotation": "test"})

        # test the endpoint
        response = c.post("/rpc/", {"jsonrpc": "2.0", "method": "get_annotations", "id": 20, "params": [project.id]},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # test the get_annotations function
        from backend.rpc import get_annotations
        annotations = get_annotations(None, project.id)
        self.assertIsNotNone(annotations)
        self.assertEqual(type(annotations), list)


class TestUsers(TestEndpoint):

    def test_list_possible_annotators(self):
        user = self.get_default_user()

        ann1 = get_user_model().objects.create(username="ann1")
        ann2 = get_user_model().objects.create(username="ann2")
        ann3 = get_user_model().objects.create(username="ann3")

        proj = Project.objects.create(owner=user)

        possible_annotators = get_possible_annotators(self.get_loggedin_request())
        self.assertEqual(len(possible_annotators), 4, "Should list all users")
        project_annotators = get_project_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(len(project_annotators), 0)

        add_project_annotator(self.get_loggedin_request(), proj.pk, ann1.username)
        add_project_annotator(self.get_loggedin_request(), proj.pk, ann2.username)
        possible_annotators = get_possible_annotators(self.get_loggedin_request())
        self.assertEqual(len(possible_annotators), 2, "Associate 2 users with a project, should list 2 users")
        project_annotators = get_project_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(len(project_annotators), 2)

        remove_project_annotator(self.get_loggedin_request(), proj.pk, ann1.username)
        possible_annotators = get_possible_annotators(self.get_loggedin_request())
        self.assertEqual(len(possible_annotators), 3, "Remove 1 user from project, should list 3 users")
        project_annotators = get_project_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(len(project_annotators), 1)


class TestUserManagement(TestEndpoint):

    def setUp(self):
        user = self.get_default_user()
        user.is_staff = True
        user.save()

        get_user_model().objects.create(username="ann1")
        get_user_model().objects.create(username="ann2")
        get_user_model().objects.create(username="ann3")

    def test_get_all_users(self):

        c = self.get_loggedin_client()

        response = self.call_rpc(c, "get_all_users")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)["result"]), 4)

    def test_get_user(self):

        c = self.get_loggedin_client()

        response = self.call_rpc(c, "get_user", "ann1")
        self.assertEqual(response.status_code, 200)

    def test_admin_update_user(self):

        c = self.get_loggedin_client()

        data = {
            "id": 2,
            "username": "ann1",
            "email": "ann1@test.com",
            "is_manager": True,
            "is_admin": False,
        }

        response = self.call_rpc(c, "admin_update_user", data)
        self.assertEqual(response.status_code, 200)


class TestAnnotationTaskManager(TestEndpoint):

    def annotation_info(self, annotation_id, message):
        annotation = Annotation.objects.get(pk=annotation_id)
        print(
            f"{message} : [annotation id] {annotation.pk} [document {annotation.document.id}] [user {annotation.user.pk}]")

    def test_annotation_task(self):
        # Create users and project, add them as annotators
        manager = self.get_default_user()
        manager_request = self.get_loggedin_request()

        ann1 = get_user_model().objects.create(username="ann1")
        ann1_request = self.get_request()
        ann1_request.user = ann1

        proj = Project.objects.create(owner=manager)
        proj.annotations_per_doc = 3
        proj.annotator_max_annotation = 0.6  # Annotator can annotator max of 60% of docs

        # Create documents
        num_docs = 10
        docs = list()
        for i in range(num_docs):
            docs.append(Document.objects.create(project=proj))

        self.assertEqual(proj.documents.count(), num_docs)

        # Get blank annotation task, user has no project association
        self.assertIsNone(get_annotation_task(ann1_request))

        # Add ann1 as the project's annotator
        self.assertTrue(add_project_annotator(manager_request, proj.id, ann1.username))

        # Reject first task
        ann1.refresh_from_db()
        task_context = get_annotation_task(ann1_request)
        rejected_id = task_context['annotation_id']
        self.annotation_info(rejected_id, "Rejected annotation")
        self.assertEqual(proj.num_occupied_tasks, 1, "Num occupied must be 1")
        reject_annotation_task(ann1_request, task_context["annotation_id"])
        self.assertEqual(proj.num_occupied_tasks, 0, "Num occupied should be zero after rejection")

        # Time out the second task
        ann1.refresh_from_db()
        task_context = get_annotation_task(ann1_request)
        timed_out_id = task_context['annotation_id']
        timed_out_annotation = Annotation.objects.get(pk=timed_out_id)
        timed_out_annotation.timed_out = timezone.now()
        timed_out_annotation.save()
        self.annotation_info(timed_out_id, "Forcing timeout")

        # Complete the rest of annotation tasks
        for i in range(6):
            ann1.refresh_from_db()
            task_context = get_annotation_task(ann1_request)
            current_annotation_id = task_context['annotation_id']
            self.annotation_info(current_annotation_id, "Annotated")

            proj.refresh_from_db()
            self.assertNotEqual(rejected_id, task_context['annotation_id'])
            self.assertIsNotNone(task_context)
            self.assertGreater(task_context["annotation_id"], 0)
            self.assertTrue(i == proj.num_completed_tasks, f"Num completed should be {i} ")
            self.assertTrue(i + 1 == proj.num_occupied_tasks, f"Num occupied should be  {i + 1}")

            second_context = get_annotation_task(ann1_request)
            proj.refresh_from_db()
            self.assertEqual(current_annotation_id, second_context['annotation_id'],
                             "Calling get task again without completing must return the same annotation task")

            complete_annotation_task(ann1_request, task_context["annotation_id"], {})
            proj.refresh_from_db()
            self.assertTrue(i + 1 == proj.num_completed_tasks, f"Num completed should be {i + 1}")
            self.assertTrue(i + 1 == proj.num_occupied_tasks, f"Num occupied should be {i + 1}")

        # Default ratio is set at 0.6 so after making 6 annotations out of 10 docs
        # we expect the 7th one to be in reach of quota
        ann1.refresh_from_db()
        task_context = get_annotation_task(ann1_request)
        self.assertIsNone(task_context)

    def test_multi_user_annotation_task(self):
        num_annotators = 5
        num_documents = 10
        num_annotations_per_doc = 5
        annotator_max_annotation = 0.6  # Annotator can annotator max of 60% of docs
        num_rejections_per_annotator = 3
        num_timeouts_per_annotator = 5

        # Create users and project, add them as annotators
        manager = self.get_default_user()
        manager_request = self.get_loggedin_request()

        annotators = [get_user_model().objects.create(username=f"annotator{i}") for i in range(num_annotators)]

        proj = Project.objects.create(owner=manager)
        proj.annotations_per_doc = num_annotations_per_doc
        proj.annotator_max_annotation = annotator_max_annotation
        proj.save()

        # Make them project annotator
        for annotator in annotators:
            self.assertTrue(add_project_annotator(manager_request, proj.id, annotator.username))

        documents = [Document.objects.create(project=proj) for i in range(num_documents)]

        for i in range(num_rejections_per_annotator):
            for annotator in annotators:
                self.reject_annotation(annotator)
                print(
                    f"Remaining/completed/total {proj.num_annotation_tasks_remaining}/{proj.num_completed_tasks}/{proj.num_annotation_tasks_total}")


        for i in range(num_annotations_per_doc + 1):
            for annotator in annotators:
                self.perform_annotation(annotator, expect_completed=proj.num_annotation_tasks_remaining < 1)
                print(
                    f"Remaining/completed/total {proj.num_annotation_tasks_remaining}/{proj.num_completed_tasks}/{proj.num_annotation_tasks_total}")

    def get_annotator_request(self, annotator):
        annotator.refresh_from_db()
        request = self.get_request()
        request.user = annotator
        return request

    def perform_annotation(self, annotator, expect_completed=False):

        request = self.get_annotator_request(annotator)

        task_context = get_annotation_task(request)

        if expect_completed:
            self.assertTrue(task_context is None)
            return

        annotation_id = task_context['annotation_id']
        self.annotation_info(annotation_id, "Annotated")

        complete_annotation_task(request, annotation_id, {})

    def reject_annotation(self, annotator):
        request = self.get_annotator_request(annotator)

        task_context = get_annotation_task(request)
        annotation_id = task_context['annotation_id']
        self.annotation_info(annotation_id, "Rejected")

        reject_annotation_task(request, annotation_id)

    def test_completing_project(self):
        """ Case where project finishes before an annotator reaches quota """
        num_annotators = 100
        num_documents = 10
        num_annotations_per_doc = 3
        num_total_tasks = num_documents * num_annotations_per_doc
        annotator_max_annotation = 0.6  # Annotator can annotator max of 60% of docs

        # Create users and project, add them as annotators
        manager = self.get_default_user()
        manager_request = self.get_loggedin_request()

        annotators = [get_user_model().objects.create(username=f"annotator{i}") for i in range(num_annotators)]

        ann1 = get_user_model().objects.create(username="ann1")
        ann1_request = self.get_request()
        ann1_request.user = ann1

        proj = Project.objects.create(owner=manager)
        proj.annotations_per_doc = num_annotations_per_doc
        proj.annotator_max_annotation = annotator_max_annotation
        proj.save()

        # Make them project annotator
        for annotator in annotators:
            self.assertTrue(add_project_annotator(manager_request, proj.id, annotator.username))

        documents = [Document.objects.create(project=proj) for i in range(num_documents)]

        annotation_count = 0
        for i in range(num_annotations_per_doc):
            for annotator in annotators:
                self.assertFalse(proj.is_completed)
                self.perform_annotation(annotator)
                annotation_count += 1
                if num_total_tasks - annotation_count < 1:
                    break

            if num_total_tasks - annotation_count < 1:
                break

        self.assertTrue(proj.is_completed)
        self.assertEqual(0, proj.annotators.count())
