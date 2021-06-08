from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase, Client
from django.test.client import RequestFactory
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

    def call_rpc(self, client, mehod_name, *params):
        response = client.post("/rpc/", {
            "jsonrpc": "2.0",
            "id": 0,
            "method": mehod_name,
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


class TestAnnotationTaskManager(TestEndpoint):

    def test_annotation_task(self):
        # Create users and project, add them as annotators
        manager = self.get_default_user()
        manager_request = self.get_loggedin_request()

        ann1 = get_user_model().objects.create(username="ann1")
        ann1_request = self.get_request()
        ann1_request.user = ann1

        ann2 = get_user_model().objects.create(username="ann2")
        ann3 = get_user_model().objects.create(username="ann3")

        proj = Project.objects.create(owner=manager)
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

        ann1.refresh_from_db()
        task_context = get_annotation_task(ann1_request)
        print(f"Trying to annotate id {task_context['annotation_id']}")
        self.assertEqual(proj.num_occupied_tasks, 1, "Num occupied must be 1")
        reject_annotation_task(ann1_request, task_context["annotation_id"])
        self.assertEqual(proj.num_occupied_tasks, 0, "Num occupied should be zero after rejection")

        rejected_id = task_context['annotation_id']

        for i in range(6):
            ann1.refresh_from_db()
            task_context = get_annotation_task(ann1_request)
            print(f"Trying to annotate id {task_context['annotation_id']}")
            current_annotation_id = task_context['annotation_id']
            self.assertNotEqual(rejected_id, task_context['annotation_id'])
            self.assertIsNotNone(task_context)
            self.assertGreater(task_context["annotation_id"], 0)
            self.assertEqual(proj.num_completed_tasks, i, "Num completed should be same as index ")
            self.assertEqual(proj.num_occupied_tasks, i + 1, "Num occupied should be same as index +1")

            second_context = get_annotation_task(ann1_request)
            self.assertEqual(current_annotation_id, second_context['annotation_id'],
                             "Calling get task again without completing must return the same annotation task")

            complete_annotation_task(ann1_request, task_context["annotation_id"], {})
            self.assertEqual(proj.num_completed_tasks, i + 1, "Num completed should be same as index +1")
            self.assertEqual(proj.num_occupied_tasks, i + 1, "Num occupied should be same as index +1")

        # Default ratio is set at 0.6 so after making 6 annotations out of 10 docs
        # we expect the 7th one to be in reach of quota
        ann1.refresh_from_db()
        task_context = get_annotation_task(ann1_request)
        self.assertIsNone(task_context)
