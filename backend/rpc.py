import secrets
import logging
import datetime

import json
import os
from urllib.parse import urljoin
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login as djlogin, logout as djlogout
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import manager
from django.core import mail
from django.db.models import Q
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
import gatenlp
from django.utils.html import strip_tags
from gatenlp import annotation_set
# https://pypi.org/project/gatenlp/

from backend.errors import AuthError
from backend.rpcserver import rpc_method, rpc_method_auth, rpc_method_manager, rpc_method_admin
from backend.models import Project, Document, DocumentType, Annotation, AnnotatorProject, AnnotationChangeHistory, \
    UserDocumentFormatPreference, document_preference_str
from backend.utils.misc import get_value_from_key_path, insert_value_to_key_path, read_custom_document
from backend.utils.serialize import ModelSerializer

log = logging.getLogger(__name__)

serializer = ModelSerializer()
User = get_user_model()

#####################################
### Initilisation                 ###
#####################################
@rpc_method
def initialise(request):
    """
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
    """
    context_object = {
        "user": is_authenticated(request),
        "configs": {
            "docFormatPref": get_user_document_pref_from_request(request)
        },
        "global_configs": {
            "allowUserDelete": settings.ALLOW_USER_DELETE
        }
    }
    return context_object

def get_user_document_pref_from_request(request):
    if request.user.is_authenticated:
        return document_preference_str(request.user.doc_format_pref)
    else:
        return document_preference_str(UserDocumentFormatPreference.JSON)

#####################################
### Login/Logout/Register Methods ###
#####################################

@rpc_method
def is_authenticated(request):
    """
    Checks that the current user has logged in.
    """
    context = {
        "isAuthenticated": False,
        "isManager": False,
        "isAdmin": False,
    }
    if request.user.is_authenticated:
        context["isAuthenticated"] = True
        context["isActivated"] = request.user.is_activated
        context["username"] = request.user.username

    if not request.user.is_anonymous:
        if request.user.is_manager or request.user.is_staff:
            context["isManager"] = True

        if request.user.is_staff:
            context["isAdmin"] = True

    return context


@rpc_method
def login(request, payload):
    context = {}
    if "username" not in payload:
        raise RuntimeError("No username provided")

    if "password" not in payload:
        raise RuntimeError("No password provided")

    user = authenticate(username=payload["username"], password=payload["password"])
    if user is not None:

        if user.is_deleted:
            raise AuthError("Cannot login with a deleted account")

        djlogin(request, user)
        context["username"] = user.username
        context["isAuthenticated"] = user.is_authenticated
        context["isManager"] = user.is_manager
        context["isAdmin"] = user.is_staff
        context["isActivated"] = user.is_activated
        return context
    else:
        raise AuthError("Invalid username or password.")


@rpc_method
def logout(request):
    djlogout(request)
    return


@rpc_method
def register(request, payload):
    context = {}
    username = payload.get("username")
    password = payload.get("password")
    email = payload.get("email")
    agreed_privacy_policy = True

    if not get_user_model().objects.filter(username=username).exists():
        user = get_user_model().objects.create_user(username=username, password=password, email=email, agreed_privacy_policy=agreed_privacy_policy)
        _generate_user_activation(user)
        djlogin(request, user)
        context["username"] = payload["username"]
        context["isAuthenticated"] = True
        context["isActivated"] = user.is_activated
        return context
    else:
        raise ValueError("Username already exists")


@rpc_method
def generate_user_activation(request, username):
    try:
        user = get_user_model().objects.get(username=username)

        if user.is_activated:
            raise ValueError(f"User {username}'s account is already activated.")

        _generate_user_activation(user)


    except User.DoesNotExist:
        log.exception(f"Trying to generate activation code for user: {username} that doesn't exist")
        raise ValueError("User does not exist.")


def _generate_user_activation(user):

    if settings.ACTIVATION_WITH_EMAIL:
        register_token = secrets.token_urlsafe(settings.ACTIVATION_TOKEN_LENGTH)
        user.activate_account_token = register_token
        user.activate_account_token_expire = timezone.now() + \
                                             datetime.timedelta(days=settings.ACTIVATION_EMAIL_TIMEOUT_DAYS)
        user.save()

        app_name = settings.APP_NAME
        activate_url_base = urljoin(settings.APP_URL, settings.ACTIVATION_URL_PATH)
        activate_url = f"{activate_url_base}?username={user.username}&token={user.activate_account_token}"
        context = {
            "app_name": app_name,
            "activate_url": activate_url,
        }

        message = render_to_string("registration_mail.html", context)

        num_sent = mail.send_mail(subject=f"Activate your account at {app_name}",
                                  message=strip_tags(message),
                                  html_message=message,
                                  from_email=settings.ADMIN_EMAIL,
                                  recipient_list=[user.email],
                                  fail_silently=False
                                  )

        if num_sent < 1:
            log.warning(f"Could not send registration email for user {user.username}")
    else:
        user.is_account_activated = True
        user.save()



@rpc_method
def activate_account(request, username, token):
    try:

        if token is None or len(token) < settings.ACTIVATION_TOKEN_LENGTH:
            log.error(f"Token of invalid length provided: {token} username: {username}")
            raise ValueError("Invalid token provided")

        user = get_user_model().objects.get(username=username, activate_account_token=token)

        if user.activate_account_token_expire < timezone.now():
            raise ValueError("Token has expired")

        user.is_account_activated = True
        user.activate_account_token = None
        user.activate_account_token_expire = None
        user.save()

    except User.DoesNotExist as e:
        log.exception(f"Activate account, invalid token provided: {token}")
        raise ValueError("Invalid token provided")


@rpc_method
def generate_password_reset(request, username):
    user = None

    try:
        user = get_user_model().objects.get(username=username)
        register_token = secrets.token_urlsafe(settings.PASSWORD_RESET_TOKEN_LENGTH)
        user.reset_password_token = register_token
        user.reset_password_token_expire = timezone.now() + \
                                           datetime.timedelta(hours=settings.PASSWORD_RESET_TIMEOUT_HOURS)
        user.save()

        app_name = settings.APP_NAME
        reset_url_base = urljoin(settings.APP_URL, settings.PASSWORD_RESET_URL_PATH)
        reset_url = f"{reset_url_base}?username={user.username}&token={user.reset_password_token}"
        context = {
            "app_name": app_name,
            "reset_url": reset_url,
        }

        message = render_to_string("password_reset_mail.html", context)

        num_sent = mail.send_mail(subject=f"Reset your password at {app_name}",
                                  message=strip_tags(message),
                                  html_message=message,
                                  from_email=settings.ADMIN_EMAIL,
                                  recipient_list=[user.email],
                                  fail_silently=False
                                  )
        if num_sent < 1:
            log.warning(f"Could not send password reset email for user {user.username}")


    except User.DoesNotExist as e:
        raise ValueError("Username does not exist.")


@rpc_method
def reset_password(request, username, token, new_password):
    try:

        if token is None or len(token) < settings.PASSWORD_RESET_TOKEN_LENGTH:
            log.error(f"Token of invalid length provided: {token} username: {username}")
            raise ValueError("Invalid token provided")

        user = get_user_model().objects.get(username=username, reset_password_token=token)
        if user.reset_password_token_expire < timezone.now():
            raise ValueError("Token has expired")

        user.set_password(new_password)
        user.reset_password_token = None
        user.reset_password_token_expire = None
        user.save()

    except User.DoesNotExist as e:
        log.exception(f"Reset password, invalid token provided: {token}")
        raise ValueError("Invalid token provided")


@rpc_method_auth
def change_password(request, payload):
    user = request.user
    user.set_password(payload.get("password"))
    user.save()
    return


@rpc_method_auth
def change_email(request, payload):
    user = request.user

    user.email = payload.get("email")
    user.is_account_activated = False  # User needs to re-verify their e-mail again
    user.save()
    _generate_user_activation(user)  # Generate
    return

@rpc_method_auth
def set_user_receive_mail_notifications(request, do_receive_notifications):
    user = request.user
    user.receive_mail_notifications = do_receive_notifications
    user.save()

@rpc_method_auth
def set_user_document_format_preference(request, doc_preference):
    user = request.user

    # Convert to enum value
    if doc_preference == "JSON":
        user.doc_format_pref = UserDocumentFormatPreference.JSON
    elif doc_preference == "CSV":
        user.doc_format_pref = UserDocumentFormatPreference.CSV
    else:
        raise ValueError(f"Document preference value {doc_preference} is invalid")

    user.save()


#############################
### User specific methods ###
#############################

@rpc_method_auth
def get_user_details(request):
    user = request.user

    data = {
        "username": user.username,
        "email": user.email,
        "created": user.created,
        "receive_mail_notifications": user.receive_mail_notifications,
    }

    user_role = "annotator"
    if user.is_staff:
        user_role = "admin"
    elif user.is_manager:
        user_role = "manager"

    data["user_role"] = user_role

    # Convert doc preference to string
    data["doc_format_pref"] = document_preference_str(user.doc_format_pref)

    return data
@rpc_method_auth
def get_user_annotated_projects(request):
    """
    Gets a list of projects that the user has annotated
    """
    user = request.user

    projects_list = []

    for project in Project.objects.filter(documents__annotations__user_id=user.pk).distinct().order_by("-id"):
        projects_list.append({
            "id": project.pk,
            "name": project.name,
            "allow_annotation_change": project.allow_annotation_change,
            "configuration": project.configuration,
        })

    return projects_list


@rpc_method_auth
def get_user_annotations_in_project(request, project_id, current_page=1, page_size=None):
    """
    Gets a list of documents in a project where the user has performed annotations in.
    :param project_id: The id of the project to query
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :returns: Dictionary of items and total count after filter is applied {"items": [], "total_count": int}
    """
    user = request.user

    if project_id is None:
        raise Exception("Must have project_id")

    if current_page < 1:
        raise Exception("Page must start from 1")
    current_page = current_page - 1  # Change to zero index


    project = Project.objects.get(pk=project_id)
    user_annotated_docs = project.documents.filter(doc_type=DocumentType.ANNOTATION,
                                                   annotations__user_id=user.pk).distinct()
    total_count = user_annotated_docs.count()

    if user_annotated_docs.count() < 1:
        raise Exception(f"No annotations in this project {project.pk}:{project.name}")

    if page_size is not None:
        start_index = current_page * page_size
        end_index = (current_page + 1) * page_size
        paginated_docs = user_annotated_docs[start_index:end_index]
    else:
        paginated_docs = user_annotated_docs

    documents_out = []
    for document in paginated_docs:
        annotations_list = [annotation.get_listing() for annotation in document.annotations.filter(user=user)]
        documents_out.append(document.get_listing(annotations_list))

    return {"items": documents_out, "total_count": total_count}


@rpc_method_auth
def user_delete_personal_information(request):
    request.user.delete_user_personal_information()


@rpc_method_auth
def user_delete_account(request):
    if settings.ALLOW_USER_DELETE:
        request.user.delete()
    else:
        raise Exception("Teamware's current configuration does not allow user accounts to be deleted.")


##################################
### Project Management Methods ###
##################################

@rpc_method_manager
def create_project(request):

    with transaction.atomic():

        proj = Project.objects.create()
        proj.owner = request.user
        proj.save()
        serialized_project = serializer.serialize(proj, exclude_fields=set(["annotators", "annotatorproject"]))
        serialized_project["annotators"] = get_project_annotators(request, proj.id)
        return serialized_project

@rpc_method_manager
def delete_project(request, project_id):
    with transaction.atomic():
        proj = Project.objects.get(pk=project_id)
        proj.delete()
        return True

@rpc_method_manager
def update_project(request, project_dict):
    with transaction.atomic():
        project = serializer.deserialize(Project, project_dict, exclude_fields=set(["annotators", "annotatorproject"]))
        return True

@rpc_method_manager
def get_project(request, project_id):
    proj = Project.objects.get(pk=project_id)
    out_proj = {
        **serializer.serialize(proj, exclude_fields=set(["annotators", "annotatorproject"])),
        **proj.get_annotators_dict(),
        **proj.get_project_stats()
    }
    return out_proj


@rpc_method_manager
def clone_project(request, project_id):
    with transaction.atomic():
        current_project = Project.objects.get(pk=project_id)
        new_project = current_project.clone(owner=request.user)
        return serializer.serialize(new_project, exclude_fields=set(["annotators", "annotatorproject"]))


@rpc_method_manager
def import_project_config(request, pk, project_dict):
    with transaction.atomic():
        serializer.deserialize(Project, {
            "id": pk,
            **project_dict
        }, Project.get_project_export_field_names())


@rpc_method_manager
def export_project_config(request, pk):
    proj = Project.objects.get(pk=pk)
    return serializer.serialize(proj, Project.get_project_export_field_names())

@rpc_method_manager
def get_projects(request, current_page=1, page_size=None, filters=None):
    """
    Gets the list of projects. Query result can be limited by using current_page and page_size and sorted
    by using filters.

    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter option used to search project, currently only string is used to search
    for project title
    :returns: Dictionary of items and total count after filter is applied {"items": [], "total_count": int}
    """

    if current_page < 1:
        raise Exception("Page index starts from 1")
    current_page = current_page - 1  # Change to 0 index for query

    projects_query = None
    total_count = 0

    # Perform filtering
    if isinstance(filters, str):
        # Search project title if is filter is a string only
        projects_query = Project.objects.filter(name__contains=filters.strip())
        total_count = projects_query.count()
    else:
        projects_query = Project.objects.all()
        total_count = projects_query.count()

    # Perform pagination
    if current_page is None or page_size is None or current_page*page_size >= total_count:
        # Returns first page if limits are None or current_page goes over index
        projects = projects_query
    else:
        start_index = current_page*page_size
        end_index = (current_page+1)*page_size
        projects = projects_query[start_index:end_index]

    # Serialize
    output_projects = []
    for proj in projects:
        out_proj = {
            **serializer.serialize(proj, {"id", "name", "created"}),
            **proj.get_annotators_dict(),
            **proj.get_project_stats()
        }
        output_projects.append(out_proj)

    return {"items": output_projects, "total_count": total_count}


def _get_project_documents(project_id, current_page=1, page_size=None, filters=None, doc_type=DocumentType.ANNOTATION):
    """
    Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size
    and sorted by using filters

    :param project_id: The id of the project that the documents belong to, is a required variable
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter currently only searches for ID of documents for project title
    :param doc_type: Integer enum representation of document type Document.[ANNOTATION, TRAINING, TEST]
    :returns: Dictionary of items and total count after filter is applied {"items": [], "total_count": int}
    """

    if project_id is None:
        raise Exception("project_id must be provided in the options")

    if current_page < 1:
        raise Exception("Page index starts from 1")
    current_page = current_page - 1  # Change to 0 index for query



    project = Project.objects.get(pk=project_id)

    documents_query = None
    total_count = 0

    # Filter
    if isinstance(filters, str):
        # Search for id
        documents_query = project.documents.filter(pk=filters.strip(), doc_type=doc_type)
        total_count = documents_query.count()
    else:
        documents_query = project.documents.filter(doc_type=doc_type).all()
        total_count = documents_query.count()

    # Paginate
    if current_page is None or page_size is None or current_page*page_size >= total_count:
        documents = documents_query.all()
    else:
        start_index = current_page * page_size
        end_index = (current_page + 1) * page_size
        documents = documents_query[start_index:end_index]

    # Serialize
    documents_out = []
    for document in documents:
        annotations_list = [a.get_listing() for a in document.annotations.all()]
        documents_out.append(document.get_listing(annotations_list))

    return {"items": documents_out, "total_count": total_count}

@rpc_method_manager
def get_project_documents(request, project_id, current_page=1, page_size=None, filters=None):
    """
    Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size
    and sorted by using filters

    :param project_id: The id of the project that the documents belong to, is a required variable
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter currently only searches for ID of documents
    for project title
    :returns: Dictionary of items and total count after filter is applied {"items": [], "total_count": int}
    """

    return _get_project_documents(project_id, current_page, page_size, filters, DocumentType.ANNOTATION)

@rpc_method_manager
def get_project_test_documents(request, project_id, current_page=1, page_size=None, filters=None):
    """
    Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size
    and sorted by using filters

    :param project_id: The id of the project that the documents belong to, is a required variable
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter currently only searches for ID of documents
    for project title
    :returns: Dictionary of items and total count after filter is applied {"items": [], "total_count": int}
    """

    return _get_project_documents(project_id, current_page, page_size, filters, DocumentType.TEST)

@rpc_method_manager
def get_project_training_documents(request, project_id, current_page=1, page_size=None, filters=None):
    """
    Gets the list of documents and its annotations. Query result can be limited by using current_page and page_size
    and sorted by using filters

    :param project_id: The id of the project that the documents belong to, is a required variable
    :param current_page: A 1-indexed page count
    :param page_size: The maximum number of items to return per query
    :param filters: Filter currently only searches for ID of documents
    for project title
    :returns: Dictionary of items and total count after filter is applied {"items": [], "total_count": int}
    """

    return _get_project_documents(project_id, current_page, page_size, filters, DocumentType.TRAINING)

def _add_project_document(project_id, document_data, doc_type=DocumentType.ANNOTATION):
    project = Project.objects.get(pk=project_id)
    document = Document.objects.create(project=project, doc_type=doc_type)
    document.data = document_data
    document.save()
    return document.pk


@rpc_method_manager
def add_project_document(request, project_id, document_data):
    with transaction.atomic():
        return _add_project_document(project_id, document_data=document_data, doc_type=DocumentType.ANNOTATION)

@rpc_method_manager
def add_project_test_document(request, project_id, document_data):
    with transaction.atomic():
        return _add_project_document(project_id, document_data=document_data, doc_type=DocumentType.TEST)

@rpc_method_manager
def add_project_training_document(request, project_id, document_data):
    with transaction.atomic():
        return _add_project_document(project_id, document_data=document_data, doc_type=DocumentType.TRAINING)

@rpc_method_manager
def add_document_annotation(request, doc_id, annotation_data):

    with transaction.atomic():
        document = Document.objects.get(pk=doc_id)
        annotation = Annotation.objects.create(document=document, user=request.user)
        annotation.data = annotation_data
        return annotation.pk


@rpc_method_manager
def get_annotations(request, project_id):
    """
    Serialize project annotations as GATENLP format JSON using the python-gatenlp interface.
    """
    project = Project.objects.get(pk=project_id)
    annotations = []
    for document in project.documents.all():
        # create a GateNLP Document instance
        doc = gatenlp.Document(text=document.data['text'])
        doc.name = str(document.pk)

        for annotation in document.annotations.all():
            # add an Annotation_Set named as the annotation user
            annset = doc.annset(name=annotation.user.username)

            # add the annotation to the annotation set
            annset.add(start=0,
                       end=len(document.data['text']),
                       anntype="Document",
                       features=dict(label=annotation.data, _id=annotation.pk),
                       )

        # For each document, append the annotations
        annotations.append(doc.save_mem(fmt="bdocjs"))

    return annotations

@rpc_method_manager
def delete_documents_and_annotations(request, doc_id_ary, anno_id_ary):
    for anno_id in anno_id_ary:
        Annotation.objects.filter(pk=anno_id).delete()

    for doc_id in doc_id_ary:
        Document.objects.filter(pk=doc_id).delete()

    return True

@rpc_method_manager
def get_possible_annotators(request, proj_id):
    project = Project.objects.get(pk=proj_id)
    # get a list of IDs of annotators that is currently active in any project
    active_annotators = User.objects.filter(annotatorproject__status=AnnotatorProject.ACTIVE).values_list('id', flat=True)
    project_annotators = project.annotators.all().values_list('id', flat=True)
    # Do an exclude filter to remove annotator with the those ids
    valid_annotators = User.objects.filter(is_deleted=False).exclude(id__in=active_annotators).exclude(id__in=project_annotators)
    output = [serializer.serialize(annotator, {"id", "username", "email"}) for annotator in valid_annotators]
    return output


@rpc_method_manager
def get_project_annotators(request, proj_id):
    project_annotators = AnnotatorProject.objects.filter(project_id=proj_id)
    output = []
    for ap in project_annotators:
        output.append({
            **serializer.serialize(ap.annotator, {"id", "username", "email"}),
            **serializer.serialize(ap, exclude_fields={"annotator", "project"}),
            **ap.get_stats()
        })
    return output


@rpc_method_manager
def add_project_annotator(request, proj_id, username):
    with transaction.atomic():
        annotator = User.objects.get(username=username)
        project = Project.objects.get(pk=proj_id)
        project.add_annotator(annotator)
        project.save()
        return True

@rpc_method_manager
def make_project_annotator_active(request, proj_id, username):
    with transaction.atomic():
        annotator = User.objects.get(username=username)
        project = Project.objects.get(pk=proj_id)
        project.make_annotator_active(annotator)
        return True


@rpc_method_manager
def project_annotator_allow_annotation(request, proj_id, username):
    with transaction.atomic():
        annotator = User.objects.get(username=username)
        project = Project.objects.get(pk=proj_id)
        project.annotator_set_allowed_to_annotate(annotator)


@rpc_method_manager
def remove_project_annotator(request, proj_id, username):
    with transaction.atomic():
        annotator = User.objects.get(username=username)
        project = Project.objects.get(pk=proj_id)
        project.remove_annotator(annotator)
        project.save()
        return True

@rpc_method_manager
def reject_project_annotator(request, proj_id, username):
    with transaction.atomic():
        annotator = User.objects.get(username=username)
        project = Project.objects.get(pk=proj_id)
        project.reject_annotator(annotator)
        project.save()
        return True

@rpc_method_manager
def get_annotation_timings(request, proj_id):
    project = Project.objects.get(pk=proj_id)

    annotation_timings = []

    documents = project.documents.select_related("project").all()

    for document in documents:
        for annotation in document.annotations.all():
            if annotation.time_to_complete:
                data_point = {'x': annotation.time_to_complete, 'y': 0}
                annotation_timings.append(data_point)

    return annotation_timings

@rpc_method_manager
def delete_annotation_change_history(request, annotation_change_history_id):
    annotation_change_history = AnnotationChangeHistory.objects.get(pk=annotation_change_history_id)
    if request.user.is_associated_with_annotation(annotation_change_history.annotation):
        if annotation_change_history.annotation.change_history.all().count() > 1:
            annotation_change_history.delete()
        else:
            raise RuntimeError("Must have at least a single annotation change history for a completed annotation.")
    else:
        raise PermissionError("No permission to access the annotation history")

###############################
### Annotator methods       ###
###############################

@rpc_method_auth
def get_annotation_task(request):
    """
    Gets the annotator's current task, returns a dictionary about the annotation task that contains all the information
    needed to render the Annotate view.
    """

    with transaction.atomic():

        # Times out any pending annotation
        Annotation.check_for_timed_out_annotations()

        # Gets project the user's associated with
        user = request.user
        project = user.annotates.filter(annotatorproject__status=AnnotatorProject.ACTIVE).distinct().first()

        # No project to annotate
        if not project:
            return None

        # Gets the annotation task or None
        return project.get_annotator_task(user)


@rpc_method_auth
def get_annotation_task_with_id(request, annotation_id):
    """
    Get annotation task dictionary for a specific annotation_id, must belong to the annotator (or is a manager or above)
    """

    with transaction.atomic():
        user = request.user
        annotation = Annotation.objects.get(pk=annotation_id)
        if not annotation.user_allowed_to_annotate(user):
            raise PermissionError(
                f"User {user.username} trying to complete annotation id {annotation_id} that doesn't belong to them")

        if annotation.document and annotation.document.project:
            return annotation.document.project.get_annotation_task_dict(annotation,
                                                                        include_task_history_in_project=False)
        else:
            raise RuntimeError(f"Could not get the annotation task with id {annotation_id}")


@rpc_method_auth
def complete_annotation_task(request, annotation_id, annotation_data, elapsed_time=None):
    """
    Complete the annotator's current task
    """

    with transaction.atomic():

        # Gets project the user's associated with
        user = request.user

        annotation = Annotation.objects.get(pk=annotation_id)
        if not annotation.user_allowed_to_annotate(user):
            raise PermissionError(
                f"User {user.username} trying to complete annotation id {annotation_id} that doesn't belong to them")

        if annotation:
            annotation.complete_annotation(annotation_data, elapsed_time)


@rpc_method_auth
def reject_annotation_task(request, annotation_id):
    """
    Reject the annotator's current task
    """

    with transaction.atomic():

        # Gets project the user's associated with
        user = request.user

        annotation = Annotation.objects.get(pk=annotation_id)
        if not annotation.user_allowed_to_annotate(user):
            raise PermissionError(
                f"User {user.username} trying to complete annotation id {annotation_id} that doesn't belong to them")

        if annotation:
            annotation.reject_annotation()

@rpc_method_auth
def change_annotation(request, annotation_id, new_data):
    """Adds annotation data to history"""
    try:
        annotation = Annotation.objects.get(pk=annotation_id)

        if annotation.document.doc_type is not DocumentType.ANNOTATION:
            raise RuntimeError("It not possible to change annotations created for testing or training documents.")


        if annotation.user_allowed_to_annotate(request.user) or request.user.is_manager_or_above():
            annotation.change_annotation(new_data, request.user)
    except Annotation.DoesNotExist:
        raise RuntimeError(f"Annotation with ID {annotation_id} does not exist")



@rpc_method_auth
def get_document(request, document_id):
    """ Obsolete: to be deleted"""
    doc = Document.objects.get(pk=document_id)
    if request.user.is_associated_with_document(doc):
        return doc.get_listing(annotation_list=[anno.get_listing() for anno in doc.annotations.all()])
    else:
        raise PermissionError("No permission to access the document")


@rpc_method_auth
def get_annotation(request, annotation_id):
    """ Obsolete: to be deleted"""
    annotation = Annotation.objects.get(pk=annotation_id)
    if request.user.is_associated_with_annotation(annotation):
        return annotation.get_listing()
    else:
        raise PermissionError("No permission to access the annotation")



@rpc_method_auth
def annotator_leave_project(request):
    """ Allow annotator to leave their currently associated project. """
    user = request.user
    project = user.active_project

    if project is None:
        raise Exception("No current active project")

    project.remove_annotator(get_user_model().objects.get(pk=user.id))


###############################
### User Management Methods ###
###############################

@rpc_method_admin
def get_all_users(request):
    users = User.objects.all()
    output = [serializer.serialize(user, {"id", "username", "email", "is_manager", "is_staff"}) for user in users]
    return output

@rpc_method_admin
def get_user(request, username):
    user = User.objects.get(username=username)

    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_manager": user.is_manager,
        "is_admin": user.is_staff,
        "is_activated": user.is_activated
    }

    return data

@rpc_method_admin
def admin_update_user(request, user_dict):
    user = User.objects.get(id=user_dict["id"])

    user.username = user_dict["username"]
    user.email = user_dict["email"]
    user.is_manager = user_dict["is_manager"]
    user.is_staff = user_dict["is_admin"]
    user.is_account_activated = user_dict["is_activated"]
    user.save()

    return user_dict


@rpc_method_admin
def admin_update_user_password(request, username, password):
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()


@rpc_method_admin
def admin_delete_user_personal_information(request, username):
    user = User.objects.get(username=username)
    user.delete_user_personal_information()


@rpc_method_admin
def admin_delete_user(request, username):
    if settings.ALLOW_USER_DELETE:
        user = User.objects.get(username=username)
        user.delete()
    else:
        raise Exception("Teamware's current configuration does not allow the deleting of users")


##################################
### Privacy Policy/T&C Methods ###
##################################

@rpc_method
def get_privacy_policy_details(request):
    details = settings.PRIVACY_POLICY

    custom_docs = {
        'CUSTOM_PP_DOCUMENT': read_custom_document(settings.CUSTOM_PP_DOCUMENT_PATH) if os.path.isfile(
            settings.CUSTOM_PP_DOCUMENT_PATH) else None,
        'CUSTOM_TC_DOCUMENT': read_custom_document(settings.CUSTOM_TC_DOCUMENT_PATH) if os.path.isfile(
            settings.CUSTOM_TC_DOCUMENT_PATH) else None
    }

    details.update(custom_docs)

    url = {
        'URL': request.headers['Host']
    }

    details.update(url)

    return details


###############################
### Utility Methods         ###
###############################

@rpc_method
def get_endpoint_listing(request):
    from .rpcserver import JSONRPCEndpoint
    return JSONRPCEndpoint.endpoint_listing()
