from django.contrib.auth import get_user_model
from django.test import TestCase, Client
import json
from backend.rpcserver import rpc_method, rpc_method_auth, AuthError
import backend.rpcserver


@rpc_method
def rpc_test_add_func(a, b):
    return a+b

@rpc_method_auth
def rpc_test_need_auth():
    return 10

@rpc_method
def rpc_test_raise_auth_error():
    raise AuthError("Raised to test authentication error handling")

@rpc_method_auth
def rpc_test_raise_permission_error():
    raise PermissionError("Thrown to test permission error handling")

class TestRPCServer(TestCase):

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


class TestRPCProjectCreate(TestCase):

    def test_rpc_update_project(self):
        username = "testuser"
        user_pass = "123456789"
        user = get_user_model().objects.create(username=username)
        user.set_password(user_pass)
        user.save()

        data = {
            "id":1,
            "name":"Test project",
            "data":"[\n  {\n    \"text\": \"Some text\"\n  },\n  {\n    \"text\": \"Document <b>with some html</b>\"\n  },\n  {\n    \"text\": \"Another document\"\n  }\n]\n",
            "configuration":"[\n  {\n    \"name\": \"sentiment\",\n    \"title\": \"Sentiment\",\n    \"type\":\"radio\",\n    \"options\": {\n        \"positive\": \"Positive\",\n        \"negative\": \"Negative\",\n        \"neutral\": \"Neutral\"\n    }\n  },\n  {\n    \"name\": \"reason\",\n    \"title\": \"Reason for your stated sentiment\",\n    \"type\":\"textarea\"\n  }\n]",
            }

        c = Client()
        response = c.post("/rpc/", {"jsonrpc": "2.0", "method": "update_project", "id": 20, "params": data},
                          content_type="application/json")
        self.assertEqual(response.status_code, 400)