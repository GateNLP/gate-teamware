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



### is_authenticated() 


::: tip Description
Checks that the current user has logged in.
:::








### login(payload) 




#### Parameters

* payload







### logout() 









### register(payload) 




#### Parameters

* payload







### generate_user_activation(username) 




#### Parameters

* username







### activate_account(username,token) 




#### Parameters

* username

* token







### generate_password_reset(username) 




#### Parameters

* username







### reset_password(username,token,new_password) 




#### Parameters

* username

* token

* new_password







### change_password(payload) <Badge text="login" type="tip" title="Requires user to be logged in"/>




#### Parameters

* payload







### change_email(payload) <Badge text="login" type="tip" title="Requires user to be logged in"/>




#### Parameters

* payload







### set_user_receive_mail_notifications(do_receive_notifications) <Badge text="login" type="tip" title="Requires user to be logged in"/>




#### Parameters

* do_receive_notifications







### get_user_details() <Badge text="login" type="tip" title="Requires user to be logged in"/>









### get_user_annotations() <Badge text="login" type="tip" title="Requires user to be logged in"/>









### create_project() <Badge text="manager" type="warning" title="Requires manager permission"/>









### update_project(project_dict) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_dict







### get_project(project_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_id







### clone_project(project_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_id







### import_project_config(pk,project_dict) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* pk

* project_dict







### export_project_config(pk) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* pk







### get_projects() <Badge text="manager" type="warning" title="Requires manager permission"/>









### get_project_documents(project_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_id







### add_project_document(project_id,document_data) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_id

* document_data







### add_document_annotation(doc_id,annotation) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* doc_id

* annotation







### get_annotations(project_id) <Badge text="manager" type="warning" title="Requires manager permission"/>


::: tip Description
Serialize project annotations as GATENLP format JSON using the python-gatenlp interface.
:::



#### Parameters

* project_id







### delete_documents_and_annotations(doc_id_ary,anno_id_ary) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* doc_id_ary

* anno_id_ary







### get_possible_annotators() <Badge text="manager" type="warning" title="Requires manager permission"/>









### get_project_annotators(proj_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id







### add_project_annotator(proj_id,username) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id

* username







### remove_project_annotator(proj_id,username) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id

* username







### get_annotation_task() <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Gets the annotator&#x27;s current task
:::








### complete_annotation_task(annotation_id,annotation_data) <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Complete the annotator&#x27;s current task, with option to get the next task
:::



#### Parameters

* annotation_id

* annotation_data







### reject_annotation_task(annotation_id) <Badge text="login" type="tip" title="Requires user to be logged in"/>




#### Parameters

* annotation_id







### get_document_content(document_id) <Badge text="login" type="tip" title="Requires user to be logged in"/>




#### Parameters

* document_id







### get_annotation_content(annotation_id) <Badge text="login" type="tip" title="Requires user to be logged in"/>




#### Parameters

* annotation_id







### get_all_users() <Badge text="admin" type="error" title="Require admin permission"/>









### get_user(username) <Badge text="admin" type="error" title="Require admin permission"/>




#### Parameters

* username







### admin_update_user(user_dict) <Badge text="admin" type="error" title="Require admin permission"/>




#### Parameters

* user_dict







### admin_update_user_password(username,password) <Badge text="admin" type="error" title="Require admin permission"/>




#### Parameters

* username

* password







### get_endpoint_listing() 











