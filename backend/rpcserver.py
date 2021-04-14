import json
import logging
from django.http import JsonResponse, HttpRequest
from django.views import View

log = logging.getLogger(__name__)

REGISTERED_RPC_METHODS = {}

PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


class JSONRPCEndpoint(View):

    def success_response(self, data, msg_id=None):
        context = {
            "jsonrpc": "2.0",
            "result": data
        }

        if msg_id is not None:
            context["id"] = msg_id

        return JsonResponse(context, status=200)

    def error_response(self, code, message, msg_id=None):
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

        return JsonResponse(context, status=400)

    def post(self, request: HttpRequest, *args, **kwargs):

        try:

            # Parse message
            msg = json.loads(request.body)

            # Check id
            msg_id = msg["id"] if "id" in msg else None

            # Check protocol header
            if "jsonrpc" not in msg or msg["jsonrpc"] != "2.0":
                log.warning(f"No jsonrpc field in request")
                return self.error_response(INVALID_REQUEST, "Not json rpc 2.0", msg_id)

            # Get method name
            method_name = None
            if "method" in msg and msg["method"] in REGISTERED_RPC_METHODS:
                method_name = msg["method"]

            if method_name is None:
                log.warning(f"No method name in request")
                return self.error_response(METHOD_NOT_FOUND, f"Method {method_name} was not found")

            # Get params
            params = msg["params"] if "params" in msg else None

            # Get and call method
            method = REGISTERED_RPC_METHODS[method_name]
            result = method(*params)
            log.info(f"Called {method_name}")
            return self.success_response(result, msg_id)
        except Exception as e:
            log.exception("Unknown exception")
            return self.error_response(INTERNAL_ERROR, f"Unknown error: {e}")


def rpc_method(func):
    REGISTERED_RPC_METHODS[func.__name__] = func
    return func
