(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{401:function(t,a,e){"use strict";e.r(a);var r=e(53),s=Object(r.a)({},(function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[e("h1",{attrs:{id:"api-documentation"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#api-documentation"}},[t._v("#")]),t._v(" API Documentation")]),t._v(" "),e("h2",{attrs:{id:"using-the-jsonrpc-endpoints"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#using-the-jsonrpc-endpoints"}},[t._v("#")]),t._v(" Using the JSONRPC endpoints")]),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("TIP")]),t._v(" "),e("p",[t._v("A single endpoint is used for all API requests, located at "),e("code",[t._v("/rpc")])])]),t._v(" "),e("p",[t._v("The API used in the app complies to JSON-RPC 2.0 spec. Requests should always be sent with "),e("code",[t._v("POST")]),t._v(" and\ncontain a JSON request object in the body. The response will also be in the form of a JSON object.")]),t._v(" "),e("p",[t._v("For example, to call the method "),e("code",[t._v("subtract(a, b)")]),t._v(". Send "),e("code",[t._v("POST")]),t._v(" a post request to "),e("code",[t._v("/rpc")]),t._v(" with the following JSON\nin the body:")]),t._v(" "),e("div",{staticClass:"language-json extra-class"},[e("pre",{pre:!0,attrs:{class:"language-json"}},[e("code",[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"jsonrpc"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token string"}},[t._v('"2.0"')]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"method"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token string"}},[t._v('"subtract"')]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"params"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),t._v("\n      "),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("42")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n      "),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("23")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"id"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("1")]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n")])])]),e("p",[t._v("Variables are passed as a list to the "),e("code",[t._v("params")]),t._v(" field, in this case "),e("code",[t._v("a=42")]),t._v(" and "),e("code",[t._v("b=23")]),t._v(". The "),e("code",[t._v("id")]),t._v(" field in the top\nlevel of the request object refers to the message ID, this ID value will be matched in the response,\nit does not affect the method that is being called.")]),t._v(" "),e("p",[t._v("The response will be as follows:")]),t._v(" "),e("div",{staticClass:"language-json extra-class"},[e("pre",{pre:!0,attrs:{class:"language-json"}},[e("code",[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"jsonrpc"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token string"}},[t._v('"2.0"')]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"result"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("19")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"id"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("1")]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n")])])]),e("p",[t._v("In the case of errors, the response will contain an "),e("code",[t._v("error")]),t._v(" field with error "),e("code",[t._v("code")]),t._v(" and error "),e("code",[t._v("message")]),t._v(":")]),t._v(" "),e("div",{staticClass:"language-json extra-class"},[e("pre",{pre:!0,attrs:{class:"language-json"}},[e("code",[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"jsonrpc"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token string"}},[t._v('"2.0"')]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"error"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n      "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"code"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("-32601")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n      "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"message"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token string"}},[t._v('"Method not found"')]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n   "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v('"id"')]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),e("span",{pre:!0,attrs:{class:"token string"}},[t._v('"1"')]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n")])])]),e("p",[t._v("The following are error codes used in the app:")]),t._v(" "),e("div",{staticClass:"language-python extra-class"},[e("pre",{pre:!0,attrs:{class:"language-python"}},[e("code",[t._v("PARSE_ERROR "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("-")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("32700")]),t._v("\nINVALID_REQUEST "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("-")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("32600")]),t._v("\nMETHOD_NOT_FOUND "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("-")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("32601")]),t._v("\nINVALID_PARAMS "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("-")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("32602")]),t._v("\nINTERNAL_ERROR "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("-")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("32603")]),t._v("\nAUTHENTICATION_ERROR "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("-")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("32000")]),t._v("\nUNAUTHORIZED_ERROR "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("-")]),e("span",{pre:!0,attrs:{class:"token number"}},[t._v("32001")]),t._v("\n")])])]),e("h2",{attrs:{id:"api-listing"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#api-listing"}},[t._v("#")]),t._v(" API Listing")]),t._v(" "),e("h3",{attrs:{id:"is-authenticated"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#is-authenticated"}},[t._v("#")]),t._v(" is_authenticated()")]),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Checks that the current user has logged in.")])]),t._v(" "),e("h3",{attrs:{id:"login-payload"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#login-payload"}},[t._v("#")]),t._v(" login(payload)")]),t._v(" "),e("h4",{attrs:{id:"parameters"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("payload")])]),t._v(" "),e("h3",{attrs:{id:"logout"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#logout"}},[t._v("#")]),t._v(" logout()")]),t._v(" "),e("h3",{attrs:{id:"register-payload"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#register-payload"}},[t._v("#")]),t._v(" register(payload)")]),t._v(" "),e("h4",{attrs:{id:"parameters-2"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-2"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("payload")])]),t._v(" "),e("h3",{attrs:{id:"generate-user-activation-username"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#generate-user-activation-username"}},[t._v("#")]),t._v(" generate_user_activation(username)")]),t._v(" "),e("h4",{attrs:{id:"parameters-3"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-3"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("username")])]),t._v(" "),e("h3",{attrs:{id:"activate-account-username-token"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#activate-account-username-token"}},[t._v("#")]),t._v(" activate_account(username,token)")]),t._v(" "),e("h4",{attrs:{id:"parameters-4"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-4"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("username")])]),t._v(" "),e("li",[e("p",[t._v("token")])])]),t._v(" "),e("h3",{attrs:{id:"generate-password-reset-username"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#generate-password-reset-username"}},[t._v("#")]),t._v(" generate_password_reset(username)")]),t._v(" "),e("h4",{attrs:{id:"parameters-5"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-5"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("username")])]),t._v(" "),e("h3",{attrs:{id:"reset-password-username-token-new-password"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#reset-password-username-token-new-password"}},[t._v("#")]),t._v(" reset_password(username,token,new_password)")]),t._v(" "),e("h4",{attrs:{id:"parameters-6"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-6"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("username")])]),t._v(" "),e("li",[e("p",[t._v("token")])]),t._v(" "),e("li",[e("p",[t._v("new_password")])])]),t._v(" "),e("h3",{attrs:{id:"change-password-payload"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#change-password-payload"}},[t._v("#")]),t._v(" change_password(payload) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-7"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-7"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("payload")])]),t._v(" "),e("h3",{attrs:{id:"change-email-payload"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#change-email-payload"}},[t._v("#")]),t._v(" change_email(payload) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-8"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-8"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("payload")])]),t._v(" "),e("h3",{attrs:{id:"set-user-receive-mail-notifications-do-receive-notifications"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#set-user-receive-mail-notifications-do-receive-notifications"}},[t._v("#")]),t._v(" set_user_receive_mail_notifications(do_receive_notifications) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-9"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-9"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("do_receive_notifications")])]),t._v(" "),e("h3",{attrs:{id:"get-user-details"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-user-details"}},[t._v("#")]),t._v(" get_user_details() "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("h3",{attrs:{id:"get-user-annotated-projects"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-user-annotated-projects"}},[t._v("#")]),t._v(" get_user_annotated_projects() "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Gets a list of projects that the user has annotated")])]),t._v(" "),e("h3",{attrs:{id:"get-user-annotations-in-project-project-id-current-page-page-size"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-user-annotations-in-project-project-id-current-page-page-size"}},[t._v("#")]),t._v(" get_user_annotations_in_project(project_id,current_page,page_size) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v('Gets a list of documents in a project where the user has performed annotations in.\n:param project_id: The id of the project to query\n:param current_page: A 1-indexed page count\n:param page_size: The maximum number of items to return per query\n:returns: Dictionary of items and total count after filter is applied {"items": [], "total_count": int}')])]),t._v(" "),e("h4",{attrs:{id:"parameters-10"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-10"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("project_id")])]),t._v(" "),e("li",[e("p",[t._v("current_page")])]),t._v(" "),e("li",[e("p",[t._v("page_size")])])]),t._v(" "),e("h3",{attrs:{id:"create-project"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#create-project"}},[t._v("#")]),t._v(" create_project() "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h3",{attrs:{id:"delete-project-project-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#delete-project-project-id"}},[t._v("#")]),t._v(" delete_project(project_id) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-11"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-11"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("project_id")])]),t._v(" "),e("h3",{attrs:{id:"update-project-project-dict"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#update-project-project-dict"}},[t._v("#")]),t._v(" update_project(project_dict) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-12"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-12"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("project_dict")])]),t._v(" "),e("h3",{attrs:{id:"get-project-project-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-project-project-id"}},[t._v("#")]),t._v(" get_project(project_id) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-13"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-13"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("project_id")])]),t._v(" "),e("h3",{attrs:{id:"clone-project-project-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#clone-project-project-id"}},[t._v("#")]),t._v(" clone_project(project_id) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-14"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-14"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("project_id")])]),t._v(" "),e("h3",{attrs:{id:"import-project-config-pk-project-dict"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#import-project-config-pk-project-dict"}},[t._v("#")]),t._v(" import_project_config(pk,project_dict) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-15"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-15"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("pk")])]),t._v(" "),e("li",[e("p",[t._v("project_dict")])])]),t._v(" "),e("h3",{attrs:{id:"export-project-config-pk"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#export-project-config-pk"}},[t._v("#")]),t._v(" export_project_config(pk) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-16"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-16"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("pk")])]),t._v(" "),e("h3",{attrs:{id:"get-projects-current-page-page-size-filters"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-projects-current-page-page-size-filters"}},[t._v("#")]),t._v(" get_projects(current_page,page_size,filters) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Gets the list of projects. Query result can be limited by using current_page and page_size and sorted\nby using filters.")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",[e("code",[t._v(":param current_page: A 1-indexed page count\n:param page_size: The maximum number of items to return per query\n:param filters: Filter option used to search project, currently only string is used to search\nfor project title\n:returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}\n")])])])]),t._v(" "),e("h4",{attrs:{id:"parameters-17"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-17"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("current_page")])]),t._v(" "),e("li",[e("p",[t._v("page_size")])]),t._v(" "),e("li",[e("p",[t._v("filters")])])]),t._v(" "),e("h3",{attrs:{id:"get-project-documents-project-id-current-page-page-size-filters"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-project-documents-project-id-current-page-page-size-filters"}},[t._v("#")]),t._v(" get_project_documents(project_id,current_page,page_size,filters) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size\nand sorted by using filters")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",[e("code",[t._v(":param project_id: The id of the project that the documents belong to, is a required variable\n:param current_page: A 1-indexed page count\n:param page_size: The maximum number of items to return per query\n:param filters: Filter currently only searches for ID of documents\nfor project title\n:returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}\n")])])])]),t._v(" "),e("h4",{attrs:{id:"parameters-18"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-18"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("project_id")])]),t._v(" "),e("li",[e("p",[t._v("current_page")])]),t._v(" "),e("li",[e("p",[t._v("page_size")])]),t._v(" "),e("li",[e("p",[t._v("filters")])])]),t._v(" "),e("h3",{attrs:{id:"get-project-test-documents-project-id-current-page-page-size-filters"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-project-test-documents-project-id-current-page-page-size-filters"}},[t._v("#")]),t._v(" get_project_test_documents(project_id,current_page,page_size,filters) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size\nand sorted by using filters")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",[e("code",[t._v(":param project_id: The id of the project that the documents belong to, is a required variable\n:param current_page: A 1-indexed page count\n:param page_size: The maximum number of items to return per query\n:param filters: Filter currently only searches for ID of documents\nfor project title\n:returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}\n")])])])]),t._v(" "),e("h4",{attrs:{id:"parameters-19"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-19"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("project_id")])]),t._v(" "),e("li",[e("p",[t._v("current_page")])]),t._v(" "),e("li",[e("p",[t._v("page_size")])]),t._v(" "),e("li",[e("p",[t._v("filters")])])]),t._v(" "),e("h3",{attrs:{id:"get-project-training-documents-project-id-current-page-page-size-filters"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-project-training-documents-project-id-current-page-page-size-filters"}},[t._v("#")]),t._v(" get_project_training_documents(project_id,current_page,page_size,filters) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size\nand sorted by using filters")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",[e("code",[t._v(":param project_id: The id of the project that the documents belong to, is a required variable\n:param current_page: A 1-indexed page count\n:param page_size: The maximum number of items to return per query\n:param filters: Filter currently only searches for ID of documents\nfor project title\n:returns: Dictionary of items and total count after filter is applied {&quot;items&quot;: [], &quot;total_count&quot;: int}\n")])])])]),t._v(" "),e("h4",{attrs:{id:"parameters-20"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-20"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("project_id")])]),t._v(" "),e("li",[e("p",[t._v("current_page")])]),t._v(" "),e("li",[e("p",[t._v("page_size")])]),t._v(" "),e("li",[e("p",[t._v("filters")])])]),t._v(" "),e("h3",{attrs:{id:"add-project-document-project-id-document-data"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#add-project-document-project-id-document-data"}},[t._v("#")]),t._v(" add_project_document(project_id,document_data) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-21"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-21"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("project_id")])]),t._v(" "),e("li",[e("p",[t._v("document_data")])])]),t._v(" "),e("h3",{attrs:{id:"add-project-test-document-project-id-document-data"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#add-project-test-document-project-id-document-data"}},[t._v("#")]),t._v(" add_project_test_document(project_id,document_data) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-22"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-22"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("project_id")])]),t._v(" "),e("li",[e("p",[t._v("document_data")])])]),t._v(" "),e("h3",{attrs:{id:"add-project-training-document-project-id-document-data"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#add-project-training-document-project-id-document-data"}},[t._v("#")]),t._v(" add_project_training_document(project_id,document_data) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-23"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-23"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("project_id")])]),t._v(" "),e("li",[e("p",[t._v("document_data")])])]),t._v(" "),e("h3",{attrs:{id:"add-document-annotation-doc-id-annotation-data"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#add-document-annotation-doc-id-annotation-data"}},[t._v("#")]),t._v(" add_document_annotation(doc_id,annotation_data) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-24"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-24"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("doc_id")])]),t._v(" "),e("li",[e("p",[t._v("annotation_data")])])]),t._v(" "),e("h3",{attrs:{id:"get-annotations-project-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-annotations-project-id"}},[t._v("#")]),t._v(" get_annotations(project_id) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Serialize project annotations as GATENLP format JSON using the python-gatenlp interface.")])]),t._v(" "),e("h4",{attrs:{id:"parameters-25"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-25"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("project_id")])]),t._v(" "),e("h3",{attrs:{id:"delete-documents-and-annotations-doc-id-ary-anno-id-ary"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#delete-documents-and-annotations-doc-id-ary-anno-id-ary"}},[t._v("#")]),t._v(" delete_documents_and_annotations(doc_id_ary,anno_id_ary) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-26"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-26"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("doc_id_ary")])]),t._v(" "),e("li",[e("p",[t._v("anno_id_ary")])])]),t._v(" "),e("h3",{attrs:{id:"get-possible-annotators-proj-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-possible-annotators-proj-id"}},[t._v("#")]),t._v(" get_possible_annotators(proj_id) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-27"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-27"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("proj_id")])]),t._v(" "),e("h3",{attrs:{id:"get-project-annotators-proj-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-project-annotators-proj-id"}},[t._v("#")]),t._v(" get_project_annotators(proj_id) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-28"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-28"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("proj_id")])]),t._v(" "),e("h3",{attrs:{id:"add-project-annotator-proj-id-username"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#add-project-annotator-proj-id-username"}},[t._v("#")]),t._v(" add_project_annotator(proj_id,username) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-29"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-29"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("proj_id")])]),t._v(" "),e("li",[e("p",[t._v("username")])])]),t._v(" "),e("h3",{attrs:{id:"make-project-annotator-active-proj-id-username"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#make-project-annotator-active-proj-id-username"}},[t._v("#")]),t._v(" make_project_annotator_active(proj_id,username) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-30"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-30"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("proj_id")])]),t._v(" "),e("li",[e("p",[t._v("username")])])]),t._v(" "),e("h3",{attrs:{id:"project-annotator-allow-annotation-proj-id-username"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#project-annotator-allow-annotation-proj-id-username"}},[t._v("#")]),t._v(" project_annotator_allow_annotation(proj_id,username) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-31"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-31"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("proj_id")])]),t._v(" "),e("li",[e("p",[t._v("username")])])]),t._v(" "),e("h3",{attrs:{id:"remove-project-annotator-proj-id-username"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#remove-project-annotator-proj-id-username"}},[t._v("#")]),t._v(" remove_project_annotator(proj_id,username) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-32"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-32"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("proj_id")])]),t._v(" "),e("li",[e("p",[t._v("username")])])]),t._v(" "),e("h3",{attrs:{id:"reject-project-annotator-proj-id-username"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#reject-project-annotator-proj-id-username"}},[t._v("#")]),t._v(" reject_project_annotator(proj_id,username) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-33"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-33"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("proj_id")])]),t._v(" "),e("li",[e("p",[t._v("username")])])]),t._v(" "),e("h3",{attrs:{id:"get-annotation-timings-proj-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-annotation-timings-proj-id"}},[t._v("#")]),t._v(" get_annotation_timings(proj_id) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-34"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-34"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("proj_id")])]),t._v(" "),e("h3",{attrs:{id:"get-annotation-task"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-annotation-task"}},[t._v("#")]),t._v(" get_annotation_task() "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Gets the annotator's current task")])]),t._v(" "),e("h3",{attrs:{id:"complete-annotation-task-annotation-id-annotation-data-elapsed-time"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#complete-annotation-task-annotation-id-annotation-data-elapsed-time"}},[t._v("#")]),t._v(" complete_annotation_task(annotation_id,annotation_data,elapsed_time) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Complete the annotator's current task, with option to get the next task")])]),t._v(" "),e("h4",{attrs:{id:"parameters-35"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-35"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("annotation_id")])]),t._v(" "),e("li",[e("p",[t._v("annotation_data")])]),t._v(" "),e("li",[e("p",[t._v("elapsed_time")])])]),t._v(" "),e("h3",{attrs:{id:"reject-annotation-task-annotation-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#reject-annotation-task-annotation-id"}},[t._v("#")]),t._v(" reject_annotation_task(annotation_id) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-36"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-36"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("annotation_id")])]),t._v(" "),e("h3",{attrs:{id:"change-annotation-annotation-id-new-data"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#change-annotation-annotation-id-new-data"}},[t._v("#")]),t._v(" change_annotation(annotation_id,new_data) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Adds annotation data to history")])]),t._v(" "),e("h4",{attrs:{id:"parameters-37"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-37"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("annotation_id")])]),t._v(" "),e("li",[e("p",[t._v("new_data")])])]),t._v(" "),e("h3",{attrs:{id:"get-document-document-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-document-document-id"}},[t._v("#")]),t._v(" get_document(document_id) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-38"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-38"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("document_id")])]),t._v(" "),e("h3",{attrs:{id:"get-annotation-annotation-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-annotation-annotation-id"}},[t._v("#")]),t._v(" get_annotation(annotation_id) "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-39"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-39"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("annotation_id")])]),t._v(" "),e("h3",{attrs:{id:"delete-annotation-change-history-annotation-change-history-id"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#delete-annotation-change-history-annotation-change-history-id"}},[t._v("#")]),t._v(" delete_annotation_change_history(annotation_change_history_id) "),e("Badge",{attrs:{text:"manager",type:"warning",title:"Requires manager permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-40"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-40"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("annotation_change_history_id")])]),t._v(" "),e("h3",{attrs:{id:"annotator-leave-project"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#annotator-leave-project"}},[t._v("#")]),t._v(" annotator_leave_project() "),e("Badge",{attrs:{text:"login",type:"tip",title:"Requires user to be logged in"}})],1),t._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[t._v("Description")]),t._v(" "),e("p",[t._v("Allow annotator to leave their currently associated project.")])]),t._v(" "),e("h3",{attrs:{id:"get-all-users"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-all-users"}},[t._v("#")]),t._v(" get_all_users() "),e("Badge",{attrs:{text:"admin",type:"error",title:"Require admin permission"}})],1),t._v(" "),e("h3",{attrs:{id:"get-user-username"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-user-username"}},[t._v("#")]),t._v(" get_user(username) "),e("Badge",{attrs:{text:"admin",type:"error",title:"Require admin permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-41"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-41"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("username")])]),t._v(" "),e("h3",{attrs:{id:"admin-update-user-user-dict"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#admin-update-user-user-dict"}},[t._v("#")]),t._v(" admin_update_user(user_dict) "),e("Badge",{attrs:{text:"admin",type:"error",title:"Require admin permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-42"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-42"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[t._v("user_dict")])]),t._v(" "),e("h3",{attrs:{id:"admin-update-user-password-username-password"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#admin-update-user-password-username-password"}},[t._v("#")]),t._v(" admin_update_user_password(username,password) "),e("Badge",{attrs:{text:"admin",type:"error",title:"Require admin permission"}})],1),t._v(" "),e("h4",{attrs:{id:"parameters-43"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#parameters-43"}},[t._v("#")]),t._v(" Parameters")]),t._v(" "),e("ul",[e("li",[e("p",[t._v("username")])]),t._v(" "),e("li",[e("p",[t._v("password")])])]),t._v(" "),e("h3",{attrs:{id:"get-endpoint-listing"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#get-endpoint-listing"}},[t._v("#")]),t._v(" get_endpoint_listing()")])])}),[],!1,null,null,null);a.default=s.exports}}]);