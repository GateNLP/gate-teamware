from django.db import transaction
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
import json

from django.test.utils import TZ_SUPPORT
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from backend.models import Annotation, Document, Project
from backend.rpcserver import rpc_method, rpc_method_auth, AuthError, rpc_method_manager, rpc_method_admin, \
    UNAUTHORIZED_ERROR, AUTHENTICATION_ERROR
import backend.rpcserver


@rpc_method
def rpc_test_add_func(request, a, b):
    return a+b

@rpc_method_auth
def rpc_test_need_auth(request):
    return 10

@rpc_method_manager
def rpc_test_need_manager(request):
    return 10

@rpc_method_admin
def rpc_test_need_admin(request):
    return 10

@rpc_method
def rpc_test_raise_auth_error(request):
    raise AuthError("Raised to test authentication error handling")

@rpc_method_auth
def rpc_test_raise_permission_error(request):
    raise PermissionError("Thrown to test permission error handling")

@rpc_method
@transaction.atomic
def rpc_test_django_atomic(request, a, b):
    return a+b


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
            self.user = get_user_model().objects.create(username=self.username,
                                                        password=self.password,
                                                        email=self.user_email)
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

class TestRPCServer(TestEndpoint):

    def test_rpc_server(self):
        username = "testuser"
        user_pass = "123456789"
        user = get_user_model().objects.create(username=username)
        user.set_password(user_pass)
        user.save()

        c = Client()

        # Blank message
        response = c.post("/rpc/", {}, content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(msg["error"]["code"], backend.rpcserver.INVALID_REQUEST)

        # Function that doesn't exist
        response = c.post("/rpc/", {"jsonrpc": "2.0", "method": "idontexist"}, content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(msg["error"]["code"], backend.rpcserver.METHOD_NOT_FOUND)


        # Invalid params
        response = c.post("/rpc/", {"jsonrpc": "2.0", "method": "rpc_test_add_func"}, content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(msg["error"]["code"], backend.rpcserver.INVALID_PARAMS)

        # Valid formed request
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "rpc_test_add_func", "params": [30, 40], "id": 20},
                          content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(msg["result"], 30+40)
        self.assertEqual(msg["id"], 20)

        # Raising auth error from inside function
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "rpc_test_raise_auth_error", "id": 20},
                          content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(msg["error"]["code"], backend.rpcserver.AUTHENTICATION_ERROR)

        # Raising permission error form inside function
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "rpc_test_raise_permission_error", "id": 20},
                          content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(msg["error"]["code"], backend.rpcserver.AUTHENTICATION_ERROR)

        # Needs authentication
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "rpc_test_need_auth", "id": 20},
                          content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(msg["error"]["code"], backend.rpcserver.AUTHENTICATION_ERROR)


        # Authenticated
        loggedin = c.login(username=username, password=user_pass)
        self.assertTrue(loggedin)
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "rpc_test_need_auth", "id": 20},
                          content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(msg["result"], 10)

        # Raising permission error from inside function after logged in
        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "rpc_test_raise_permission_error", "id": 20},
                          content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(msg["error"]["code"], backend.rpcserver.UNAUTHORIZED_ERROR)

    def test_rpc_django_atomic(self):
        c = Client()

        response = c.post("/rpc/",
                          {"jsonrpc": "2.0", "method": "rpc_test_django_atomic", "params": [30, 40], "id": 20},
                          content_type="application/json")
        msg = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(msg["result"], 30 + 40)
        self.assertEqual(msg["id"], 20)

    def test_endpoint_auth_and_permissions(self):
        client = Client()

        annotator_username = "annotator"
        manager_username = "manager"
        admin_username = "admin"
        password = "12345678test*"

        annotator_user = get_user_model().objects.create(username=annotator_username,
                                                       email="annote@localhost.com",
                                                       is_account_activated=True)
        annotator_user.set_password(password)
        annotator_user.save()

        manager_user = get_user_model().objects.create(username=manager_username,
                                                     email="manager@localhost.com",
                                                     is_account_activated=True,
                                                     is_manager=True)
        manager_user.set_password(password)
        manager_user.save()

        admin_user = get_user_model().objects.create(username=admin_username,
                                                     email="admin@localhost.com",
                                                     is_account_activated=True,
                                                     is_staff=True,
                                                     is_superuser=True,
                                                     is_manager=True)
        admin_user.set_password(password)
        admin_user.save()

        # Not logged in
        response = self.call_rpc(client, "rpc_test_need_auth")
        self.assertEqual(response.status_code, 401)
        msg = json.loads(response.content)
        self.assertEqual(msg["error"]["code"], AUTHENTICATION_ERROR)

        response = self.call_rpc(client, "rpc_test_need_manager")
        self.assertEqual(response.status_code, 401)
        msg = json.loads(response.content)
        self.assertEqual(msg["error"]["code"], AUTHENTICATION_ERROR)

        response = self.call_rpc(client, "rpc_test_need_admin")
        self.assertEqual(response.status_code, 401)
        msg = json.loads(response.content)
        self.assertEqual(msg["error"]["code"], AUTHENTICATION_ERROR)

        # Logged in as annotator
        self.assertTrue(client.login(username=annotator_username, password=password))
        response = self.call_rpc(client, "rpc_test_need_auth")
        self.assertEqual(response.status_code, 200)

        response = self.call_rpc(client, "rpc_test_need_manager")
        self.assertEqual(response.status_code, 401)
        msg = json.loads(response.content)
        self.assertEqual(msg["error"]["code"], UNAUTHORIZED_ERROR)

        response = self.call_rpc(client, "rpc_test_need_admin")
        self.assertEqual(response.status_code, 401)
        msg = json.loads(response.content)
        self.assertEqual(msg["error"]["code"], UNAUTHORIZED_ERROR)


        # Logged in as manager
        self.assertTrue(client.login(username=manager_username, password=password))
        response = self.call_rpc(client, "rpc_test_need_auth")
        self.assertEqual(response.status_code, 200)

        response = self.call_rpc(client, "rpc_test_need_manager")
        self.assertEqual(response.status_code, 200)

        response = self.call_rpc(client, "rpc_test_need_admin")
        self.assertEqual(response.status_code, 401)
        msg = json.loads(response.content)
        self.assertEqual(msg["error"]["code"], UNAUTHORIZED_ERROR)


        # Logged in as admin
        self.assertTrue(client.login(username=admin_username, password=password))
        response = self.call_rpc(client, "rpc_test_need_auth")
        self.assertEqual(response.status_code, 200)

        response = self.call_rpc(client, "rpc_test_need_manager")
        self.assertEqual(response.status_code, 200)

        response = self.call_rpc(client, "rpc_test_need_admin")
        self.assertEqual(response.status_code, 200)




