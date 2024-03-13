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



### initialise() 


::: tip Description
Provide the initial context information to initialise the Teamware app

    context_object:
        user:
            isAuthenticated: bool
            isManager: bool
            isAdmin: bool
        configs:
            docFormatPref: bool
        global_configs:
            allowUserDelete: bool
:::








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







### set_user_document_format_preference(doc_preference) <Badge text="login" type="tip" title="Requires user to be logged in"/>




#### Parameters

* doc_preference







### get_user_details() <Badge text="login" type="tip" title="Requires user to be logged in"/>









### get_user_annotated_projects() <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Gets a list of projects that the user has annotated
:::








### get_user_annotations_in_project(project_id,current_page,page_size) <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Gets a list of documents in a project where the user has performed annotations in.
    :param project_id: The id of the project to query
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}
:::



#### Parameters

* project_id

* current_page

* page_size







### user_delete_personal_information() <Badge text="login" type="tip" title="Requires user to be logged in"/>









### user_delete_account() <Badge text="login" type="tip" title="Requires user to be logged in"/>









### create_project() <Badge text="manager" type="warning" title="Requires manager permission"/>









### delete_project(project_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_id







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







### get_projects(current_page,page_size,filters) <Badge text="manager" type="warning" title="Requires manager permission"/>


::: tip Description
Gets the list of projects. Query result can be limited by using current_page and page_size and sorted
    by using filters.

    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter option used to search project, currently only string is used to search
    for project title
    :returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}
:::



#### Parameters

* current_page

* page_size

* filters







### get_project_documents(project_id,current_page,page_size,filters) <Badge text="manager" type="warning" title="Requires manager permission"/>


::: tip Description
Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size
    and sorted by using filters

    :param project_id: The id of the project that the documents belong to, is a required variable
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter currently only searches for ID of documents
    for project title
    :returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}
:::



#### Parameters

* project_id

* current_page

* page_size

* filters







### get_project_test_documents(project_id,current_page,page_size,filters) <Badge text="manager" type="warning" title="Requires manager permission"/>


::: tip Description
Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size
    and sorted by using filters

    :param project_id: The id of the project that the documents belong to, is a required variable
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter currently only searches for ID of documents
    for project title
    :returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}
:::



#### Parameters

* project_id

* current_page

* page_size

* filters







### get_project_training_documents(project_id,current_page,page_size,filters) <Badge text="manager" type="warning" title="Requires manager permission"/>


::: tip Description
Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size
    and sorted by using filters

    :param project_id: The id of the project that the documents belong to, is a required variable
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter currently only searches for ID of documents
    for project title
    :returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}
:::



#### Parameters

* project_id

* current_page

* page_size

* filters







### add_project_document(project_id,document_data) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_id

* document_data







### add_project_test_document(project_id,document_data) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_id

* document_data







### add_project_training_document(project_id,document_data) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* project_id

* document_data







### add_document_annotation(doc_id,annotation_data) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* doc_id

* annotation_data







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







### get_possible_annotators(proj_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id







### get_project_annotators(proj_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id







### add_project_annotator(proj_id,username) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id

* username







### make_project_annotator_active(proj_id,username) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id

* username







### project_annotator_allow_annotation(proj_id,username) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id

* username







### remove_project_annotator(proj_id,username) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id

* username







### reject_project_annotator(proj_id,username) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id

* username







### get_annotation_timings(proj_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* proj_id







### delete_annotation_change_history(annotation_change_history_id) <Badge text="manager" type="warning" title="Requires manager permission"/>




#### Parameters

* annotation_change_history_id







### get_annotation_task() <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Gets the annotator&#x27;s current task, returns a dictionary about the annotation task that contains all the information
    needed to render the Annotate view.
:::








### get_annotation_task_with_id(annotation_id) <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Get annotation task dictionary for a specific annotation_id, must belong to the annotator (or is a manager or above)
:::



#### Parameters

* annotation_id







### complete_annotation_task(annotation_id,annotation_data,elapsed_time) <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Complete the annotator&#x27;s current task
:::



#### Parameters

* annotation_id

* annotation_data

* elapsed_time







### reject_annotation_task(annotation_id) <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Reject the annotator&#x27;s current task
:::



#### Parameters

* annotation_id







### change_annotation(annotation_id,new_data) <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Adds annotation data to history
:::



#### Parameters

* annotation_id

* new_data







### get_document(document_id) <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Obsolete: to be deleted
:::



#### Parameters

* document_id







### get_annotation(annotation_id) <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Obsolete: to be deleted
:::



#### Parameters

* annotation_id







### annotator_leave_project() <Badge text="login" type="tip" title="Requires user to be logged in"/>


::: tip Description
Allow annotator to leave their currently associated project.
:::








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







### admin_delete_user_personal_information(username) <Badge text="admin" type="error" title="Require admin permission"/>




#### Parameters

* username







### admin_delete_user(username) <Badge text="admin" type="error" title="Require admin permission"/>




#### Parameters

* username







### get_privacy_policy_details() 









### get_endpoint_listing() 











