---
sidebarDepth: 3
---

# API Documentation

## Using the JSONRPC endpoints

::: tip
A single endpoint is used for all API requests, located at `/rpc`
:::

The API used in the app complies to JSON-RPC 2.0 spec. Requests should always be sent with `POST` and 
contain a JSON request object in the body. The response will also be in the form of a JSON object. 

For example, to call the method `subtract(a, b)`. Send `POST` a post request to `/rpc` with the following JSON 
in the body:

```json
{
   "jsonrpc":"2.0",
   "method":"subtract",
   "params":[
      42,
      23
   ],
   "id":1
}
```

Variables are passed as a list to the `params` field, in this case `a=42` and `b=23`. The `id` field in the top
level of the request object refers to the message ID, this ID value will be matched in the response, 
it does not affect the method that is being called.

The response will be as follows:

```json
{
   "jsonrpc":"2.0",
   "result":19,
   "id":1
}
```

In the case of errors, the response will contain an `error` field with error `code` and error `message`:

```json
{
   "jsonrpc":"2.0",
   "error":{
      "code":-32601,
      "message":"Method not found"
   },
   "id":"1"
}
```

The following are error codes used in the app:

```python
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603
AUTHENTICATION_ERROR = -32000
UNAUTHORIZED_ERROR = -32001
```

## API Listing

{% for name, props in api_dict.items %}

### {{name}}({{props.all_args}}) {% if props.require_admin %}<Badge text="admin" type="error" title="Require admin permission"/>{% elif props.require_manager %}<Badge text="manager" type="warning" title="Requires manager permission"/>{% elif props.require_authentication %}<Badge text="login" type="tip" title="Requires user to be logged in"/>{% endif %}

{% if props.description.strip %}
::: tip Description
{{props.description.strip}}
:::
{% endif %}

{% if props.arguments %}
#### Parameters
{% for argname in props.arguments %}
* {{argname}}
{% endfor %}
{% endif %}



{% endfor %}



