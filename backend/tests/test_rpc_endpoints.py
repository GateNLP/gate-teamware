from django.core import mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from django.http import HttpRequest
from django.test import TestCase, Client

from django.utils import timezone
import json

from backend.models import Annotation, Document, DocumentType, Project, AnnotatorProject
from backend.rpc import create_project, update_project, add_project_document, add_document_annotation, \
    get_possible_annotators, add_project_annotator, remove_project_annotator, get_project_annotators, \
    get_annotation_task, complete_annotation_task, reject_annotation_task, register, activate_account, \
    generate_password_reset, reset_password, generate_user_activation, change_password, change_email, \
    set_user_receive_mail_notifications, delete_documents_and_annotations, import_project_config, export_project_config, \
    clone_project, delete_project, get_projects, get_project_documents, get_user_annotated_projects, \
    get_user_annotations_in_project, add_project_test_document, add_project_training_document, \
    get_project_training_documents, get_project_test_documents, project_annotator_allow_annotation, \
    annotator_leave_project, login, change_annotation, delete_annotation_change_history
from backend.rpcserver import rpc_method
from backend.errors import AuthError


from backend.tests.test_rpc_server import TestEndpoint




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

class TestAppCreatedUserAccountsCannotLogin(TestEndpoint):

    def test_app_created_user_accounts_cannot_login(self):

        # Create a user programmatically, without password
        created_user = get_user_model().objects.create(username="doesnotexist")

        # Default password is blank ""
        self.assertEqual("", created_user.password)

        with self.assertRaises(AuthError, msg="Should raise an error if logging in with None as password"):
            login(self.get_request(), {"username": "doesnotexist", "password": None})

        with self.assertRaises(AuthError, msg="Should raise an error if logging in with blank as password"):
            login(self.get_request(), {"username": "doesnotexist", "password": ""})



class TestUserRegistration(TestEndpoint):

    def test_user_registration(self):
        # Force e-mail activation
        with self.settings(ACTIVATION_WITH_EMAIL=True):
            username = "testuser"
            user_pass = "123456789"
            user_email = "test@test.com"

            # Register user, will have e-mail activation
            self.call_rpc(self.get_client(), "register", {
                "username": username,
                "password": user_pass,
                "email": user_email
            })

            # Check that mail is sent
            self.assertTrue(len(mail.outbox) > 0, "Mail to user must have been sent")

            test_user = get_user_model().objects.get(username=username)

            # Check that a token has been generated with length specified by the settings
            self.assertTrue(len(test_user.activate_account_token) > settings.ACTIVATION_TOKEN_LENGTH)
            self.assertTrue(test_user.activate_account_token_expire > timezone.now())

            with self.assertRaises(ValueError, msg="Should raise an error if user doesn't exist"):
                activate_account(self.get_request(), "doesnotexist", "tokendoesnotexist")

            with self.assertRaises(ValueError, msg="Should raise error if token is wrong or expired"):
                activate_account(self.get_request(), test_user.username, "tokendoesnotexist")

            with self.assertRaises(ValueError, msg="Should raise an error if token doesn't exist"):
                activate_account(self.get_request(), test_user.username, None)

            with self.assertRaises(ValueError, msg="Should raise an error if token is blank"):
                activate_account(self.get_request(), test_user.username, "")

            # Should activate properly this time
            activate_account(self.get_request(), test_user.username, test_user.activate_account_token)

            #  Gets user again, now should be activate
            test_user.refresh_from_db()
            self.assertTrue(test_user.is_account_activated)
            self.assertTrue(test_user.activate_account_token is None)
            self.assertTrue(test_user.activate_account_token_expire is None)

    def test_generate_user_activation(self):
        # Force e-mail activation
        with self.settings(ACTIVATION_WITH_EMAIL=True):

            with self.assertRaises(ValueError, msg="Raise an error if user doesn't exist"):
                generate_user_activation(self.get_request(), "doesnotexist")

            # Gets a test user
            test_user = self.get_default_user()

            # Generates
            generate_user_activation(self.get_request(), test_user.username)

            test_user.refresh_from_db()
            self.assertTrue(len(test_user.activate_account_token) > settings.ACTIVATION_TOKEN_LENGTH)
            self.assertTrue(test_user.activate_account_token_expire > timezone.now())


            test_user.is_account_activated = True
            test_user.save()

            with self.assertRaises(ValueError, msg="Raises an error if user is already activated"):
                generate_user_activation(self.get_request(), test_user.username)



class TestUserPasswordReset(TestEndpoint):

    def test_user_password_reset(self):
        new_password = "testNewPassword12345"

        test_user = self.get_default_user()

        # Raise error if username is wrong
        with self.assertRaises(ValueError):
            generate_password_reset(self.get_request(), "doesnotexist")

        # Should now generate a password reset token
        self.call_rpc(self.get_client(), "generate_password_reset", test_user.username)



        # Check that token generaet is valid
        test_user.refresh_from_db()
        self.assertTrue(len(test_user.reset_password_token) > settings.ACTIVATION_TOKEN_LENGTH)
        self.assertTrue(test_user.reset_password_token_expire > timezone.now())

        # Check that mail is sent
        self.assertTrue(len(mail.outbox) > 0)

        # Should raise error if token is wrong or expired
        with self.assertRaises(ValueError):
            reset_password(self.get_request(), test_user.username, "tokendoesnotexist", new_password)

        with self.assertRaises(ValueError):
            reset_password(self.get_request(), test_user.username, None, new_password)

        with self.assertRaises(ValueError):
            reset_password(self.get_request(), test_user.username, "", new_password)


        # Should now be able to reset password
        reset_password(self.get_request(), test_user.username, test_user.reset_password_token, new_password)

        #  Gets user again, now should now reset the password
        test_user.refresh_from_db()
        self.assertTrue(check_password(new_password, test_user.password))
        self.assertTrue(test_user.reset_password_token is None)
        self.assertTrue(test_user.reset_password_token_expire is None)

class TestUserConfig(TestEndpoint):

    def test_change_password(self):
        changed_password = "1234567test*"
        change_password(self.get_loggedin_request(), {"password": changed_password})
        user = self.get_default_user()
        user.refresh_from_db()
        self.assertTrue(check_password(changed_password, user.password))

    def test_change_email(self):
        changed_email = "test@mailchange.com"
        change_email(self.get_loggedin_request(), {"email": changed_email})
        user = self.get_default_user()
        user.refresh_from_db()
        self.assertEqual(user.email, changed_email)

    def test_change_receive_mail_notification(self):
        user = self.get_default_user()

        set_user_receive_mail_notifications(self.get_loggedin_request(), False)
        user.refresh_from_db()
        self.assertEqual(user.receive_mail_notifications, False)

        set_user_receive_mail_notifications(self.get_loggedin_request(), True)
        user.refresh_from_db()
        self.assertEqual(user.receive_mail_notifications, True)



class TestProject(TestEndpoint):

    def test_create_project(self):
        proj_obj = create_project(self.get_loggedin_request())
        self.assertIsNotNone(proj_obj)
        self.assertTrue('id' in proj_obj)
        self.assertTrue(proj_obj['id'] > 0)
        self.assertTrue('name' in proj_obj)

        saved_proj = Project.objects.get(pk=proj_obj['id'])
        self.assertEqual(saved_proj.owner.pk, self.get_default_user().pk)  # Owner is project creator

    def test_delete_project(self):
        """
        Test to make sure that a deleted project will remove associated documents and annotations. It should
        also remove annotators from the project.
        """

        self.assertEqual(Project.objects.all().count(), 0, "A project already exists")
        self.assertEqual(Document.objects.all().count(), 0, "Documents already exist")
        self.assertEqual(Annotation.objects.all().count(), 0, "Annotation already exists")

        proj = Project.objects.create()
        for i in range(10):
            doc = Document.objects.create(project=proj)
            for i in range(10):
                annotation = Annotation.objects.create(document=doc,)

        self.assertEqual(Project.objects.all().count(), 1, "Must have 1 project")
        self.assertEqual(Document.objects.all().count(), 10, "Must have 10 documents")
        self.assertEqual(Annotation.objects.all().count(), 100, "Must have 100 total annotations")

        def create_user_and_add_to_project(i, proj):
            user = get_user_model().objects.create(username=f"annotator_{i}")
            user.annotates.add(proj)
            user.save()
            return user

        annotators = [create_user_and_add_to_project(i, proj) for i in range(10)]

        delete_project(self.get_loggedin_request(), project_id=proj.pk)

        self.assertEqual(Project.objects.all().count(), 0, "Must have no project")
        self.assertEqual(Document.objects.all().count(), 0, "All documents should have been deleted")
        self.assertEqual(Annotation.objects.all().count(), 0, "All annotations should have been deleted")
        for annotator in annotators:
            annotator.refresh_from_db()
            self.assertEqual(annotator.annotates.filter(annotatorproject__status=AnnotatorProject.ACTIVE).first(), None, "Annotator should have been removed from the deleted project")


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

    def test_import_project_config(self):
        project = Project.objects.create()

        data = {
            "name": "Test project",
            "description": "Desc",
            "annotator_guideline": "Test guideline",
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
            "annotations_per_doc": 4,
            "annotator_max_annotation": 0.8,
            "annotation_timeout": 50,
            "document_input_preview": {
                "text": "Doc text"
            }
        }

        import_project_config(self.get_loggedin_request(), project.pk, data)

        project.refresh_from_db()

        self.assertEqual(project.name, data["name"])
        self.assertEqual(project.description, data["description"])
        self.assertEqual(project.annotator_guideline, data["annotator_guideline"])
        self.assertListEqual(project.configuration, data["configuration"])
        self.assertEqual(project.annotations_per_doc, data["annotations_per_doc"])
        self.assertEqual(project.annotator_max_annotation, data["annotator_max_annotation"])
        self.assertEqual(project.annotation_timeout, data["annotation_timeout"])
        self.assertDictEqual(project.document_input_preview, data["document_input_preview"])


    def test_export_project_config(self):
        project = Project.objects.create()
        data = {
            "id": project.pk,
            "name": "Test project",
            "description": "Desc",
            "annotator_guideline": "Test guideline",
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
            "annotations_per_doc": 4,
            "annotator_max_annotation": 0.8,
            "annotation_timeout": 50,
            "document_input_preview": {
                "text": "Doc text"
            }
        }
        update_project(self.get_loggedin_request(), data)
        config_export_dict = export_project_config(self.get_loggedin_request(), project.pk)

        self.assertEqual(config_export_dict["name"], data["name"])
        self.assertEqual(config_export_dict["description"], data["description"])
        self.assertEqual(config_export_dict["annotator_guideline"], data["annotator_guideline"])
        self.assertListEqual(config_export_dict["configuration"], data["configuration"])
        self.assertEqual(config_export_dict["annotations_per_doc"], data["annotations_per_doc"])
        self.assertEqual(config_export_dict["annotator_max_annotation"], data["annotator_max_annotation"])
        self.assertEqual(config_export_dict["annotation_timeout"], data["annotation_timeout"])
        self.assertDictEqual(config_export_dict["document_input_preview"], data["document_input_preview"])

    def test_clone_project(self):
        project = Project.objects.create()
        data = {
            "id": project.pk,
            "name": "Test project",
            "description": "Desc",
            "annotator_guideline": "Test guideline",
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
            "annotations_per_doc": 4,
            "annotator_max_annotation": 0.8,
            "annotation_timeout": 50,
            "document_input_preview": {
                "text": "Doc text"
            }
        }
        update_project(self.get_loggedin_request(), data)
        project.refresh_from_db()

        # Add some documents to the project
        for i in range(5):
            Document.objects.create(project=project, doc_type=DocumentType.TRAINING)
        for i in range(10):
            Document.objects.create(project=project, doc_type=DocumentType.TEST)
        for i in range(20):
            Document.objects.create(project=project, doc_type=DocumentType.ANNOTATION)

        self.assertEqual(5, project.num_training_documents)
        self.assertEqual(10, project.num_test_documents)
        self.assertEqual(20, project.num_documents)

        # Add annotator to project
        ann1 = get_user_model().objects.create(username="ann1")
        project.add_annotator(ann1)

        self.assertEqual(1, project.annotators.all().count())

        cloned_project_dict = clone_project(self.get_loggedin_request(), project.pk)
        cloned_project = Project.objects.get(pk=cloned_project_dict["id"])
        self.assertNotEqual(project.pk, cloned_project.pk)
        for field_name in Project.project_config_fields:
            if field_name == "name":
                self.assertEqual("Copy of " + getattr(project, field_name),  getattr(cloned_project, field_name))
            else:
                self.assertEqual(getattr(project, field_name), getattr(cloned_project, field_name))

        # Must not have associated documents
        self.assertEqual(0, cloned_project.num_training_documents)
        self.assertEqual(0, cloned_project.num_test_documents)
        self.assertEqual(0, cloned_project.num_documents)

        # Must not have associated users
        self.assertEqual(0, cloned_project.annotators.all().count())


    def test_get_projects(self):


        num_projects = 10
        for i in range(num_projects):
            Project.objects.create(name=f"Project {i}", owner=self.get_default_user())

        result = get_projects(self.get_loggedin_request())
        self.assertEqual(len(result["items"]), num_projects)
        self.assertEqual(result["total_count"], num_projects)

        page_size = 5

        # Get page 1
        result = get_projects(self.get_loggedin_request(), 1, page_size)
        self.assertEqual(len(result["items"]), page_size)
        self.assertEqual(result["total_count"], num_projects)

        # Get page 2
        result = get_projects(self.get_loggedin_request(), 2, page_size)
        self.assertEqual(len(result["items"]), page_size)
        self.assertEqual(result["total_count"], num_projects)

        # Get with filtering
        result = get_projects(self.get_loggedin_request(), 1, page_size, "8")  # Get project with no. 8 in title
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["total_count"], 1)








class TestDocument(TestEndpoint):

    def test_create_document(self):

        proj = Project.objects.create(owner=self.get_default_user())
        doc_obj = {
            "text": "Document text"
        }
        test_doc_obj = {
            "text": "Test document text"
        }
        train_doc_obj = {
            "text": "Train document text"
        }

        # Check docs count
        proj.refresh_from_db()
        self.assertEqual(0, proj.num_documents)
        self.assertEqual(0, proj.num_test_documents)
        self.assertEqual(0, proj.num_training_documents)

        # Adding annotation doc, check for content
        doc_id = add_project_document(self.get_loggedin_request(), proj.pk, doc_obj)
        self.assertTrue(doc_id > 0)

        doc = Document.objects.get(pk=doc_id)
        self.assertEqual(doc.project.pk, proj.pk)
        self.assertEqual(doc.data["text"], doc_obj["text"])  # Data check

        # Adding 2 test doc, check first doc for content
        test_doc_id = add_project_test_document(self.get_loggedin_request(), proj.pk, test_doc_obj)
        add_project_test_document(self.get_loggedin_request(), proj.pk, test_doc_obj)
        self.assertTrue(test_doc_id > 0)

        test_doc = Document.objects.get(pk=test_doc_id)
        self.assertEqual(test_doc.project.pk, proj.pk)
        self.assertEqual(test_doc.data["text"], test_doc_obj["text"])  # Data check

        # Adding 3 train doc, check first one for content
        train_doc_id = add_project_training_document(self.get_loggedin_request(), proj.pk, train_doc_obj)
        add_project_training_document(self.get_loggedin_request(), proj.pk, train_doc_obj)
        add_project_training_document(self.get_loggedin_request(), proj.pk, train_doc_obj)
        self.assertTrue(train_doc_id > 0)

        train_doc = Document.objects.get(pk=train_doc_id)
        self.assertEqual(train_doc.project.pk, proj.pk)
        self.assertEqual(train_doc.data["text"], train_doc_obj["text"])  # Data check

        # Check docs count
        proj.refresh_from_db()
        self.assertEqual(1, proj.num_documents)
        self.assertEqual(2, proj.num_test_documents)
        self.assertEqual(3, proj.num_training_documents)



    def test_get_project_documents(self):
        num_projects = 10
        num_docs_per_project = 20
        num_train_docs_per_project = 10
        num_test_docs_per_project = 15
        num_annotations_per_doc = 5
        for i in range(num_projects):
            project = Project.objects.create(name=f"Project {i}", owner=self.get_default_user())

            # Annotation docs
            for j in range(num_docs_per_project):
                doc = Document.objects.create(project=project, doc_type=DocumentType.ANNOTATION)
                for k in range(num_annotations_per_doc):
                    annotation = Annotation.objects.create(document=doc, user=self.get_default_user())
            # Training docs
            for j in range(num_train_docs_per_project):
                doc = Document.objects.create(project=project, doc_type=DocumentType.TRAINING)
                for k in range(num_annotations_per_doc):
                    annotation = Annotation.objects.create(document=doc, user=self.get_default_user())

            # Test docs
            for j in range(num_test_docs_per_project):
                doc = Document.objects.create(project=project, doc_type=DocumentType.TEST)
                for k in range(num_annotations_per_doc):
                    annotation = Annotation.objects.create(document=doc, user=self.get_default_user())

        # Gets all docs in a project
        result = get_project_documents(self.get_loggedin_request(), 1)
        self.assertEqual(len(result["items"]), num_docs_per_project)
        self.assertEqual(result["total_count"], num_docs_per_project)

        # Paginate docs
        page_size = 5
        num_pages = 4
        for i in range(num_pages):
            result = get_project_documents(self.get_loggedin_request(), 1, i+1, page_size)
            self.assertEqual(len(result["items"]), page_size)
            self.assertEqual(result["total_count"], num_docs_per_project)

        # Gets all training docs in a project
        result = get_project_training_documents(self.get_loggedin_request(), 1)
        self.assertEqual(len(result["items"]), num_train_docs_per_project)
        self.assertEqual(result["total_count"], num_train_docs_per_project)

        # Paginate training docs
        page_size = 5
        num_pages = 2
        for i in range(num_pages):
            result = get_project_training_documents(self.get_loggedin_request(), 1, i + 1, page_size)
            self.assertEqual(len(result["items"]), page_size)
            self.assertEqual(result["total_count"], num_train_docs_per_project)

        # Gets all test docs in a project
        result = get_project_test_documents(self.get_loggedin_request(), 1)
        self.assertEqual(len(result["items"]), num_test_docs_per_project)
        self.assertEqual(result["total_count"], num_test_docs_per_project)

        # Paginate test docs
        page_size = 5
        num_pages = 3
        for i in range(num_pages):
            result = get_project_test_documents(self.get_loggedin_request(), 1, i + 1, page_size)
            self.assertEqual(len(result["items"]), page_size)
            self.assertEqual(result["total_count"], num_test_docs_per_project)






class TestAnnotation(TestEndpoint):

    def test_add_annotation(self):
        proj = Project.objects.create(owner=self.get_default_user())
        doc = Document.objects.create(project=proj)

        initial_annotation_data = {"label1": "Annotation content", "label2": "Someothercontent"}

        annote_id = add_document_annotation(self.get_loggedin_request(),
                                            doc.pk,
                                            initial_annotation_data)

        annotation = Annotation.objects.get(pk=annote_id)
        self.assertEqual(annotation.user.pk, self.get_default_user().pk)  # Annotation linked to user
        self.assertDictEqual(annotation.data, initial_annotation_data)  # Data check


class TestDocumentAndAnnotation(TestEndpoint):
    def test_delete_document_and_annotation(self):
        proj = Project.objects.create(owner=self.get_default_user())
        doc = Document.objects.create(project=proj)
        annote = Annotation.objects.create(document=doc)
        annote2 = Annotation.objects.create(document=doc)


        self.assertTrue(Document.objects.count() == 1, "Must have a document")
        self.assertTrue(Annotation.objects.count() == 2, "Must have 2 annotations")

        delete_documents_and_annotations(self.get_loggedin_request(), [], [annote2.pk])
        self.assertTrue(Annotation.objects.count() == 1, "Must have 1 annotation")

        delete_documents_and_annotations(self.get_loggedin_request(), [doc.pk], [])
        self.assertTrue(Document.objects.count() == 0, "Must have 0 documents")
        self.assertTrue(Annotation.objects.count() == 0, "Must have 0 annotations")




class TestAnnotationExport(TestEndpoint):

    def test_rpc_get_annotations_endpoint(self):
        user = self.get_default_user()
        user.is_manager = True
        user.is_account_activated = True
        user.save()
        c = self.get_loggedin_client()

        ##setup
        project = Project.objects.create()

        with open('examples/documents.json') as f:
            for input_document in json.load(f):
                document = Document.objects.create(project=project, data=input_document)
                annotation = Annotation.objects.create(user=user, document=document)
                annotation.data = {"testannotation": "test"}

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
        proj2 = Project.objects.create(owner=user)


        # Listing all annotators for project 1 and 2 without anyone added to project
        possible_annotators = get_possible_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(4, len(possible_annotators), "Should list all users")
        possible_annotators = get_possible_annotators(self.get_loggedin_request(), proj_id=proj2.pk)
        self.assertEqual(4, len(possible_annotators), "Should list all users")
        project_annotators = get_project_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(0, len(project_annotators))

        # Add two project annotators to project 1
        add_project_annotator(self.get_loggedin_request(), proj.pk, ann1.username)
        add_project_annotator(self.get_loggedin_request(), proj.pk, ann2.username)
        possible_annotators = get_possible_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(2, len(possible_annotators), "Associate 2 users with a project, should list 2 users")
        possible_annotators = get_possible_annotators(self.get_loggedin_request(), proj_id=proj2.pk)
        self.assertEqual(2, len(possible_annotators), "Associate 2 users with a project, should list 2 users")
        project_annotators = get_project_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(2, len(project_annotators))

        # Remove a an annotator form project 1
        remove_project_annotator(self.get_loggedin_request(), proj.pk, ann1.username)
        possible_annotators = get_possible_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(2, len(possible_annotators), "Remove 1 user from project, should still list 2 users")
        possible_annotators = get_possible_annotators(self.get_loggedin_request(), proj_id=proj2.pk)
        self.assertEqual(3, len(possible_annotators), "Remove 1 user from project 2, should list 3 users")
        project_annotators = get_project_annotators(self.get_loggedin_request(), proj_id=proj.pk)
        self.assertEqual(2, len(project_annotators))

class TestUserAnnotationList(TestEndpoint):
    def test_get_user_annotated_projects(self):
        user = self.get_default_user()

        # Create a project with user annotation
        project = Project.objects.create(name="Test project", owner=user)
        num_docs = 30
        num_test_docs = 10
        num_train_docs = 15
        num_annotations = 10
        current_num_annotation = 0


        # Create documents with certain number of annotations
        for i in range(num_docs):
            doc = Document.objects.create(project=project)
            if current_num_annotation < num_annotations:
                annotation = Annotation.objects.create(document=doc, user=user, status=Annotation.COMPLETED)
                current_num_annotation += 1

        # Create test and train documents with an annoation each
        for i in range(num_test_docs):
            doc = Document.objects.create(project=project, doc_type=DocumentType.TEST)
            Annotation.objects.create(document=doc, user=user, status=Annotation.COMPLETED)

        for i in range(num_train_docs):
            doc = Document.objects.create(project=project, doc_type=DocumentType.TRAINING)
            Annotation.objects.create(document=doc, user=user, status=Annotation.COMPLETED)


        # Create projects without annotations
        for i in range(10):
            Project.objects.create(name=f"No annotation {i}", owner=user)

        # Only a single project has the user's annotation
        projects_list = get_user_annotated_projects(self.get_loggedin_request())
        self.assertEqual(len(projects_list), 1)


        # Gets all docs with annotation
        result = get_user_annotations_in_project(self.get_loggedin_request(), projects_list[0]["id"], 1)
        self.assertEqual(len(result["items"]), num_annotations)
        self.assertEqual(result["total_count"], num_annotations)
        for doc in result["items"]:
            self.assertEqual("Annotation", doc["doc_type"])

        # Gets paginated results
        page_size = 5
        result = get_user_annotations_in_project(self.get_loggedin_request(), projects_list[0]["id"], 1, page_size)
        self.assertEqual(len(result["items"]), page_size)
        self.assertEqual(result["total_count"], num_annotations)

        result = get_user_annotations_in_project(self.get_loggedin_request(), projects_list[0]["id"], 2, page_size)
        self.assertEqual(len(result["items"]), page_size)
        self.assertEqual(result["total_count"], num_annotations)







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
            "is_activated": False
        }

        response = self.call_rpc(c, "admin_update_user", data)
        self.assertEqual(response.status_code, 200)

    def test_admin_change_user_password(self):
        changed_password = "1234567test*"
        c = self.get_loggedin_client()
        self.call_rpc(c, "admin_update_user_password", "ann1", changed_password)

        ann1_user = get_user_model().objects.get(username="ann1")
        self.assertTrue(check_password(changed_password, ann1_user.password))




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

    def test_allowed_to_annotate(self):
        """
        add_project_annotator allows annotators to perform annotation on real dataset by default if there's no
        testing or training stages
        """

        # Create users and project, add them as annotators
        manager = self.get_default_user()
        manager_request = self.get_loggedin_request()

        ann1 = get_user_model().objects.create(username="ann1")
        ann1_request = self.get_request()
        ann1_request.user = ann1


        proj = Project.objects.create(owner=manager)


        # Create documents
        num_docs = 10
        for i in range(num_docs):
            Document.objects.create(project=proj)


        # Add ann1 as the proj_test_stage's annotator and get task, allowed to annotate by default if
        # there's no testing or training stages
        self.assertTrue(add_project_annotator(manager_request, proj.id, ann1.username))
        self.assertTrue(get_annotation_task(ann1_request))


    def test_task_rejection(self):
        """
        User should be removed from the project if they don't have more tasks due to rejecting
        documents.
        """

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

        # Add ann1 as the project's annotator
        self.assertTrue(add_project_annotator(manager_request, proj.id, ann1.username))
        ann1.refresh_from_db()


        # Reject all tasks
        for i in range(num_docs+1):
            task_context = get_annotation_task(ann1_request)

            if task_context is None:
                ann1.refresh_from_db()
                self.assertTrue(ann1.annotates.filter(annotatorproject__status=AnnotatorProject.ACTIVE).distinct().first() is None)
                return
            else:
                reject_annotation_task(ann1_request, task_context["annotation_id"])

        self.assertTrue(False, "All documents rejected but annotator still getting annotation tasks")




    def test_multi_user_annotation_task(self):
        num_annotators = 10
        num_documents = 10
        num_annotations_per_doc = 5
        annotator_max_annotation = 0.6  # Annotator can annotator max of 60% of docs

        # Create users and project, add them as annotators
        manager = self.get_default_user()
        manager_request = self.get_loggedin_request()

        annotators = [get_user_model().objects.create(username=f"annotator{i}") for i in range(num_annotators)]

        proj = Project.objects.create(owner=manager)
        proj.annotations_per_doc = num_annotations_per_doc
        proj.annotator_max_annotation = annotator_max_annotation
        proj.save()

        # Make them project annotator and allow them to annotate
        for annotator in annotators:
            self.assertTrue(add_project_annotator(manager_request, proj.id, annotator.username))

        documents = [Document.objects.create(project=proj) for i in range(num_documents)]


        for i in range(num_annotations_per_doc + 1):
            for annotator in annotators:
                self.perform_annotation(annotator, expect_completed=proj.num_annotation_tasks_remaining < 1)
                print(
                    f"Remaining/completed/total {proj.num_annotation_tasks_remaining}/{proj.num_completed_tasks}/{proj.num_annotation_tasks_total}")


        proj.refresh_from_db()
        self.assertEqual(proj.num_annotation_tasks_remaining, 0, "There must be no remaining tasks")

        for doc in documents:
            doc.refresh_from_db()
            self.assertEqual(doc.num_completed_annotations, proj.annotations_per_doc, "Documents must have exact number of annotations when finished")

            user_id_set = set()
            for anno in doc.annotations.filter(status=Annotation.COMPLETED):
                self.assertFalse(anno.user.pk in user_id_set, "Annotator must only annotate a document once")
                user_id_set.add(anno.user.pk)

            print(f"Doc ID: {doc.pk} completed_annotations: {doc.num_completed_annotations} annotator_ids: {','.join(str(v) for v in user_id_set)}")


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

        if task_context: #ignore if annotation task returned is None
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

        # Make them project annotator and allow to annotate
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
        self.assertEqual(0, proj.num_annotators)

    def test_leave_project(self):
        """ Tests a case where user leaves the project they're active in"""

        # Create project and add annotator
        project = Project.objects.create()
        annotator = get_user_model().objects.create(username="annotator")
        annotator2 = get_user_model().objects.create(username="annotator2")
        project.add_annotator(annotator)

        # They should be marked as active
        annotator_proj = AnnotatorProject.objects.get(project=project, annotator=annotator)
        self.assertEqual(AnnotatorProject.ACTIVE, annotator_proj.status,
                         "Annotator status should be marked as active")

        # Leave project
        req = self.get_loggedin_request()
        req.user = annotator
        annotator_leave_project(req)

        # Should be marked as complete
        annotator_proj.refresh_from_db()
        self.assertEqual(AnnotatorProject.COMPLETED, annotator_proj.status,
                         "Annotator status should be marked as completed")

        # Should raise an exception if user is not associated with project
        with self.assertRaises(Exception):
            req.user = annotator2
            annotator_leave_project(req)




class TestAnnotationTaskManagerTrainTestMode(TestEndpoint):
    def setUp(self):
        # Create users and project, add them as annotators
        self.manager = self.get_default_user()
        self.manager_request = self.get_loggedin_request()

        self.ann1 = get_user_model().objects.create(username="ann1")
        self.ann1_request = self.get_request()
        self.ann1_request.user = self.ann1

        self.proj = Project.objects.create(owner=self.manager)
        self.proj.annotations_per_doc = 3
        self.proj.annotator_max_annotation = 0.6  # Annotator can annotator max of 60% of docs
        # Example sentiment config, single label
        self.proj.configuration = [
          {
            "name": "htmldisplay",
            "type": "html",
            "text": "{{{text}}}"
          },
          {
            "name": "sentiment",
            "type": "radio",
            "title": "Sentiment",
            "description": "Please select a sentiment of the text above.",
            "options": {
              "negative": "Negative",
              "neutral": "Neutral",
              "positive": "Positive"
            }
          }
        ]
        self.proj.save()

        # Create documents
        self.num_docs = 20
        self.docs = []
        for i in range(self.num_docs):
            self.docs.append(Document.objects.create(project=self.proj, data={
                "text": f"Document {i}"
            }))

        # Create training documents
        self.num_training_docs = 5
        self.training_docs = []
        for i in range(self.num_training_docs):
            self.docs.append(Document.objects.create(project=self.proj,
                                                     doc_type=DocumentType.TRAINING,
                                                     data={
                                                        "text": f"Document {i}",
                                                         "gold": {
                                                             "sentiment": {
                                                                 "value": "positive",
                                                             }
                                                         }
                                                    }))



        # Create test document
        self.num_test_docs = 10
        self.test_docs = []
        for i in range(self.num_test_docs):
            self.docs.append(Document.objects.create(project=self.proj,
                                                     doc_type=DocumentType.TEST,
                                                     data={
                                                         "text": f"Document {i}",
                                                         "gold": {
                                                             "sentiment": {
                                                                 "value": "positive",
                                                             }
                                                         }
                                                     }))

    def test_annotation_task_with_training_only(self):

        self.proj.has_training_stage = True
        self.proj.has_test_stage = False
        self.proj.can_annotate_after_passing_training_and_test = False
        self.proj.save()

        # Add annotator 1 to project
        self.assertTrue(add_project_annotator(self.manager_request, self.proj.id, self.ann1.username))

        # Complete training annotations
        self.assertEqual(self.num_training_docs, self.complete_annotations(self.num_training_docs, "Training"))

        # Expect perfect score
        self.proj.refresh_from_db()
        self.assertEqual(self.num_training_docs,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TRAINING))

        # No task until annotator is allowed to annotate
        self.assertFalse("annotation_id" in get_annotation_task(self.ann1_request))
        project_annotator_allow_annotation(self.manager_request, self.proj.id, self.ann1.username)
        self.assertTrue(get_annotation_task(self.ann1_request))

        # Then complete the task normally
        self.assertEqual(self.proj.max_num_task_per_annotator, self.complete_annotations(self.num_docs, "Annotation"))

        self.assertEqual(0, self.proj.num_annotator_task_remaining(self.ann1))


    def test_annotation_task_with_training_only_auto_annotate(self):

        self.proj.has_training_stage = True
        self.proj.has_test_stage = False
        self.proj.can_annotate_after_passing_training_and_test = True
        self.proj.save()

        # Add annotator 1 to project
        self.assertTrue(add_project_annotator(self.manager_request, self.proj.id, self.ann1.username))

        # Complete training annotations
        self.assertEqual(self.num_training_docs, self.complete_annotations(self.num_training_docs, "Training"))

        # Expect perfect score
        self.proj.refresh_from_db()
        self.assertEqual(self.num_training_docs,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TRAINING))

        # No task until annotator is allowed to annotate
        self.assertTrue(get_annotation_task(self.ann1_request))

        # Then complete the task normally
        self.assertEqual(self.proj.max_num_task_per_annotator, self.complete_annotations(self.num_docs, "Annotation"))

        self.assertEqual(0, self.proj.num_annotator_task_remaining(self.ann1))

    def test_annotation_task_with_test_only(self):

        self.proj.has_training_stage = False
        self.proj.has_test_stage = True
        self.proj.can_annotate_after_passing_training_and_test = False
        self.proj.save()

        # Add annotator 1 to project
        self.assertTrue(add_project_annotator(self.manager_request, self.proj.id, self.ann1.username))

        # Complete test annotations
        self.assertEqual(self.num_test_docs, self.complete_annotations(self.num_test_docs, "Test"))

        # Expect perfect score
        self.proj.refresh_from_db()
        self.assertEqual(self.num_test_docs,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TEST))

        # No task until annotator is allowed to annotate
        self.assertFalse("annotation_id" in get_annotation_task(self.ann1_request))
        project_annotator_allow_annotation(self.manager_request, self.proj.id, self.ann1.username)
        self.assertTrue(get_annotation_task(self.ann1_request))

        # Then complete the task normally
        self.assertEqual(self.proj.max_num_task_per_annotator, self.complete_annotations(self.num_docs, "Annotation"))

        self.assertEqual(0, self.proj.num_annotator_task_remaining(self.ann1))

    def test_annotation_task_with_test_and_train(self):

        self.proj.has_training_stage = True
        self.proj.has_test_stage = True
        self.proj.can_annotate_after_passing_training_and_test = False
        self.proj.save()

        # Add annotator 1 to project
        self.assertTrue(add_project_annotator(self.manager_request, self.proj.id, self.ann1.username))

        # Complete training annotations
        self.assertEqual(self.num_training_docs, self.complete_annotations(self.num_training_docs, "Training"))

        # Expect perfect score
        self.proj.refresh_from_db()
        self.assertEqual(self.num_training_docs,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TRAINING))

        # Complete test annotations
        self.assertEqual(self.num_test_docs, self.complete_annotations(self.num_test_docs, "Test"))

        # Expect perfect score
        self.proj.refresh_from_db()
        self.assertEqual(self.num_test_docs,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TEST))

        # No task until annotator is allowed to annotate
        self.assertFalse("annotation_id" in get_annotation_task(self.ann1_request))
        project_annotator_allow_annotation(self.manager_request, self.proj.id, self.ann1.username)
        self.assertTrue(get_annotation_task(self.ann1_request))

        # Then complete the task normally
        self.assertEqual(self.proj.max_num_task_per_annotator, self.complete_annotations(self.num_docs, "Annotation"))

        self.assertEqual(0, self.proj.num_annotator_task_remaining(self.ann1))


    def test_annotation_task_with_test_and_train_auto_pass(self):

        self.proj.has_training_stage = True
        self.proj.has_test_stage = True
        self.proj.min_test_pass_threshold = 1.0
        self.proj.can_annotate_after_passing_training_and_test = True
        self.proj.save()

        # Add annotator 1 to project
        self.assertTrue(add_project_annotator(self.manager_request, self.proj.id, self.ann1.username))

        # Complete training annotations
        self.assertEqual(self.num_training_docs, self.complete_annotations(self.num_training_docs, "Training"))

        # Expect perfect score
        self.proj.refresh_from_db()
        self.assertEqual(self.num_training_docs,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TRAINING))

        # Complete test annotations
        self.assertEqual(self.num_test_docs, self.complete_annotations(self.num_test_docs, "Test"))

        # Expect perfect score
        self.proj.refresh_from_db()
        self.assertEqual(self.num_test_docs,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TEST))

        # Pass mark above threshold elevates user to annotator
        self.assertTrue(get_annotation_task(self.ann1_request))

        # Then complete the task normally
        self.assertEqual(self.proj.max_num_task_per_annotator, self.complete_annotations(self.num_docs, "Annotation"))

        self.assertEqual(0, self.proj.num_annotator_task_remaining(self.ann1))


    def test_annotation_task_with_test_and_train_auto_pass_fail(self):

        self.proj.has_training_stage = True
        self.proj.has_test_stage = True
        self.proj.min_test_pass_threshold = 0.6
        self.proj.can_annotate_after_passing_training_and_test = True
        self.proj.save()

        # Add annotator 1 to project
        self.assertTrue(add_project_annotator(self.manager_request, self.proj.id, self.ann1.username))

        # Complete training annotations
        self.assertEqual(self.num_training_docs, self.complete_annotations(self.num_training_docs, "Training"))

        # Expect perfect score
        self.proj.refresh_from_db()
        self.assertEqual(self.num_training_docs,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TRAINING))

        # Complete test annotations
        self.assertEqual(self.num_test_docs, self.complete_annotations(self.num_test_docs, "Test", use_wrong_answer=True))

        # Expect zero score, user not elevated to annotator
        self.proj.refresh_from_db()
        self.assertEqual(0,
                         self.proj.get_annotator_document_score(self.ann1, DocumentType.TEST))

        # No task until annotator is allowed to annotate
        self.assertFalse("annotation_id" in get_annotation_task(self.ann1_request))
        project_annotator_allow_annotation(self.manager_request, self.proj.id, self.ann1.username)
        self.assertTrue(get_annotation_task(self.ann1_request))

        # Then complete the task normally
        self.assertEqual(self.proj.max_num_task_per_annotator, self.complete_annotations(self.num_docs, "Annotation"))

        self.assertEqual(0, self.proj.num_annotator_task_remaining(self.ann1))


    def complete_annotations(self, num_annotations_to_complete, expected_doc_type_str, use_wrong_answer=False):

        answer = "positive"
        if use_wrong_answer:
            answer = "negative"

        # Expect to get self.num_training_docs tasks
        num_completed_tasks = 0
        for i in range(num_annotations_to_complete):
            task_context = get_annotation_task(self.ann1_request)
            if task_context:
                self.assertEqual(expected_doc_type_str, task_context["document_type"])
                complete_annotation_task(self.ann1_request, task_context["annotation_id"], {"sentiment": answer})
                num_completed_tasks += 1

        return num_completed_tasks

class TestAnnotationChange(TestEndpoint):


    def test_change_annotation_history(self):
        # Create initial project with annotation
        project = Project.objects.create(name="Test1")
        doc = Document.objects.create(project=project)
        annotation = Annotation.objects.create(document=doc,
                                               user=self.get_default_user()
                                               )

        initial_annotation_data = {
            "label": "Test annotation 1"
        }

        new_annotation_data = {
            "label": "Changed annotation"
        }

        # Fails if tries to change before the annotation is marked as completed
        with self.assertRaises(RuntimeError):
            change_annotation(self.get_loggedin_request(), annotation_id=annotation.pk, new_data=new_annotation_data)


        # Compete the annotation
        annotation.complete_annotation(initial_annotation_data)
        annotation.refresh_from_db()

        # Checks that the data goes into the change list
        self.assertEqual(1, annotation.change_history.all().count(), "Must already have 1 data history item")
        self.assertDictEqual(initial_annotation_data, annotation.data)

        # Tries to change annotation
        change_annotation(self.get_loggedin_request(), annotation_id=annotation.pk, new_data=new_annotation_data)

        self.assertEqual(2, annotation.change_history.all().count(), "Must have 2 data history items")
        self.assertDictEqual(new_annotation_data, annotation.data)


        # Fails for testing document, not allowed to change
        test_doc = Document.objects.create(project=project, doc_type=DocumentType.TEST)
        test_annotation = Annotation.objects.create(document=test_doc)
        test_annotation.complete_annotation(initial_annotation_data)


        with self.assertRaises(RuntimeError):
            change_annotation(self.get_loggedin_request(), test_annotation.pk, new_annotation_data)

        # Fails for training document, not allowed to change
        train_doc = Document.objects.create(project=project, doc_type=DocumentType.TRAINING)
        train_annotation = Annotation.objects.create(document=train_doc)
        train_annotation.complete_annotation(initial_annotation_data)

        with self.assertRaises(RuntimeError):
            change_annotation(self.get_loggedin_request(), train_annotation.pk, new_annotation_data)

    def test_delete_annotation_change_history(self):
        # Create initial project with annotation
        project = Project.objects.create(name="Test1")
        doc = Document.objects.create(project=project)
        annotation = Annotation.objects.create(document=doc,
                                               user=self.get_default_user()
                                               )

        initial_annotation_data = {
            "label": "Test annotation 1"
        }

        new_annotation_data = {
            "label": "Changed annotation"
        }

        # Complete the annotation and change once
        annotation.complete_annotation(initial_annotation_data)
        annotation.change_annotation(new_annotation_data)

        self.assertEqual(2, annotation.change_history.all().count(), "Must have 2 change entries")

        delete_annotation_change_history(self.get_loggedin_request(),
                                         annotation_change_history_id=annotation.change_history.first().pk)

        # Raises an error if there's only one entry left, should not be able to delete
        with self.assertRaises(RuntimeError):
            delete_annotation_change_history(self.get_loggedin_request(),
                                             annotation_change_history_id=annotation.change_history.first().pk)










