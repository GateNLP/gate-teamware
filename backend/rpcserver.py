import json
import logging
import inspect
from json.decoder import JSONDecodeError

from django.http import JsonResponse, HttpRequest
from django.views import View

from backend.errors import AuthError

log = logging.getLogger(__name__)

REGISTERED_RPC_METHODS = {}

PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603
AUTHENTICATION_ERROR = -32000
UNAUTHORIZED_ERROR = -32001



class RPCMethod:
    def __init__(self, function, authenticate, requires_manager=False, requires_admin=False):
        self.function = function
        self.authenticate = authenticate
        self.requires_manager = requires_manager
        self.requires_admin = requires_admin


class JSONRPCEndpoint(View):

    @staticmethod
    def endpoint_listing():
        endpoints_list = {}
        for func_name, rmethod in REGISTERED_RPC_METHODS.items():

            argspec = inspect.getfullargspec(rmethod.function)
            args_list = []
            if len(argspec.args) > 1:
                args_list = argspec.args[1:]


            endpoints_list[func_name] = {
                "description": rmethod.function.__doc__,
                "arguments": args_list,
                "defaults": argspec.defaults,
                "require_authentication": rmethod.authenticate,
                "require_manager": rmethod.requires_manager,
                "require_admin": rmethod.requires_admin
            }

        return endpoints_list


    def success_response(self, data, msg_id=None, http_status=200):
        context = {
            "jsonrpc": "2.0",
            "result": data
        }

        if msg_id is not None:
            context["id"] = msg_id

        return JsonResponse(context, status=http_status)

    def error_response(self, code, message, msg_id=None, http_status=400):
        context = {
            "jsonrpc": "2.0",
            "error":
                {
                    "code": code,
                    "message": message,
                }
        }

        if msg_id is not None:
            context["id"] = msg_id

        return JsonResponse(context, status=http_status)

    def post(self, request: HttpRequest, *args, **kwargs):

        msg_id = None
        method_name = None
        params = []

        try:

            # Parse message
            msg = json.loads(request.body)

            # Check id
            if "id" in msg:
                msg_id = msg["id"]

                # Check protocol header
            if "jsonrpc" not in msg or msg["jsonrpc"] != "2.0":
                log.warning(f"No jsonrpc field in request")
                return self.error_response(INVALID_REQUEST, "Not json rpc 2.0", msg_id, http_status=400)

            # Get method name
            if "method" in msg:
                method_name = msg["method"]

            if method_name not in REGISTERED_RPC_METHODS:
                log.warning(f"No method name {method_name} in request")
                return self.error_response(METHOD_NOT_FOUND, f"Method {method_name} was not found", http_status=405)

            # Get params
            if "params" in msg:
                params = msg["params"]

            # Get and call method
            method = REGISTERED_RPC_METHODS[method_name]

            # Check user role
            if method.authenticate and not request.user.is_authenticated:
                raise AuthError("Must be logged in to perform this operation.")

            if method.requires_manager and not (request.user.is_manager or request.user.is_staff or request.user.is_superuser):
                raise PermissionError("Must be a manager to perform this operation.")

            if method.requires_admin and not (request.user.is_staff or request.user.is_superuser):
                raise PermissionError("Must be a admin to perform this operation.")


            result = method.function(request, *params)
            log.info(f"Called {method_name}")
            return self.success_response(result, msg_id)


        except JSONDecodeError as e:
            log.exception(f"Unable to parse json string from request body {request.body}")
            return self.error_response(PARSE_ERROR, "Invalid JSON format in request")

        except ValueError as e:
            log.exception(f"Value error on rpc function {method_name}")
            return self.error_response(INVALID_REQUEST, f"{e}", http_status=400)

        except TypeError as e:
            log.exception(f"Type error on rpc function {method_name}")
            return self.error_response(INVALID_PARAMS, f"{e}", http_status=400)

        except RuntimeError as e:
            log.exception(f"Runtime error on rpc function {method_name}")
            return self.error_response(INVALID_REQUEST, f"{e}", http_status=400)

        except AuthError as e:
            log.exception(f"Authentication failed trying to access {method_name}")
            return self.error_response(AUTHENTICATION_ERROR, f"{e}", http_status=401)

        except PermissionError as e:
            log.exception(f"Not allowed to use rpc function {method_name}")
            return self.error_response(UNAUTHORIZED_ERROR, f"Permission Denied: {e}", http_status=401)

        except Exception as e:
            log.exception(f"Unknown rpc exception on method  {method_name}")
            return self.error_response(INTERNAL_ERROR, f"Unknown error: {e}", http_status=500)


def rpc_method(func):
    """
    Used as a decorator. Register the method to the list of RPC functions available.

    The decorated function can throw PermissionError or AuthError which will be converted
    to the correct error code automatically.
    """
    REGISTERED_RPC_METHODS[func.__name__] = RPCMethod(func, False)
    return func


def rpc_method_auth(func):
    """
    Used as a decorator. Register the method to the list of RPC functions available,
    authentication check is performed automatically.

    The decorated function can throw PermissionError or AuthError which will be converted
    to the correct error code automatically.
    """
    REGISTERED_RPC_METHODS[func.__name__] = RPCMethod(func, True)
    return func

def rpc_method_manager(func):
    """
    Used as a decorator. Register the method to the list of RPC functions available,
    authentication check is performed automatically.

    The decorated function can throw PermissionError or AuthError which will be converted
    to the correct error code automatically.
    """
    REGISTERED_RPC_METHODS[func.__name__] = RPCMethod(func, True, requires_manager=True)
    return func


def rpc_method_admin(func):
    """
    Used as a decorator. Register the method to the list of RPC functions available,
    authentication check is performed automatically.

    The decorated function can throw PermissionError or AuthError which will be converted
    to the correct error code automatically.
    """
    REGISTERED_RPC_METHODS[func.__name__] = RPCMethod(func, True, requires_manager=True, requires_admin=True)
    return func
