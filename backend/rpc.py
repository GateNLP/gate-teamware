import secrets
import logging
import datetime

import json
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
from backend.models import Project, Document, Annotation, AnnotatorProject
from backend.utils.misc import get_value_from_key_path, insert_value_to_key_path
from backend.utils.serialize import ModelSerializer

log = logging.getLogger(__name__)

serializer = ModelSerializer()
User = get_user_model()


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
    user = authenticate(username=payload["username"], password=payload["password"])
    if user is not None:
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

    if not get_user_model().objects.filter(username=username).exists():
        user = get_user_model().objects.create_user(username=username, password=password, email=email)
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
    user_annotated_docs = project.documents.filter(annotations__user_id=user.pk).distinct()
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


##################################
### Project Management Methods ###
##################################

@rpc_method_manager
def create_project(request):

    with transaction.atomic():

        proj = Project.objects.create()
        proj.owner = request.user
        proj.save()

        return serializer.serialize(proj)

@rpc_method_manager
def delete_project(request, project_id):
    with transaction.atomic():
        proj = Project.objects.get(pk=project_id)
        proj.delete()
        return True

@rpc_method_manager
def update_project(request, project_dict):
    with transaction.atomic():
        project = serializer.deserialize(Project, project_dict)
        return True

@rpc_method_manager
def get_project(request, project_id):
    proj = Project.objects.get(pk=project_id)
    out_proj = {
        **serializer.serialize(proj),
        **proj.get_project_stats()
    }
    return out_proj



@rpc_method_manager
def clone_project(request, project_id):
    with transaction.atomic():
        current_project = Project.objects.get(pk=project_id)
        new_project = Project.objects.create()
        new_project.owner = request.user
        for field_name in Project.project_config_fields:
            if field_name == "name":
                setattr(new_project, field_name, "Copy of " + getattr(current_project, field_name))
            else:
                setattr(new_project, field_name, getattr(current_project, field_name))
        new_project.save()

        return serializer.serialize(new_project)



@rpc_method_manager
def import_project_config(request, pk, project_dict):
    with transaction.atomic():
        serializer.deserialize(Project, {
            "id": pk,
            **project_dict
        }, Project.project_config_fields)


@rpc_method_manager
def export_project_config(request, pk):
    proj = Project.objects.get(pk=pk)
    return serializer.serialize(proj, Project.project_config_fields)

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
            **proj.get_project_stats()
        }
        output_projects.append(out_proj)

    return {"items": output_projects, "total_count": total_count}


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
        documents_query = project.documents.filter(pk=filters.strip())
        total_count = documents_query.count()
    else:
        documents_query = project.documents.all()
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
def add_project_document(request, project_id, document_data):

    with transaction.atomic():
        project = Project.objects.get(pk=project_id)
        document = Document.objects.create(project=project)
        document.data = document_data
        document.save()

        return document.pk


@rpc_method_manager
def add_document_annotation(request, doc_id, annotation):

    with transaction.atomic():
        document = Document.objects.get(pk=doc_id)
        annotation = Annotation.objects.create(document=document, data=annotation, user=request.user)
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
def get_possible_annotators(request):
    annotators = User.objects.filter(annotates=None)
    output = [serializer.serialize(annotator, {"id", "username", "email"}) for annotator in annotators]
    return output


@rpc_method_manager
def get_project_annotators(request, proj_id):
    project = Project.objects.get(pk=proj_id)
    output = [serializer.serialize(annotator, {"id", "username", "email"}) for annotator in project.annotators.all()]
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
def remove_project_annotator(request, proj_id, username):
    with transaction.atomic():
        annotator = User.objects.get(username=username)
        project = Project.objects.get(pk=proj_id)
        project.remove_annotator(annotator)
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

###############################
### Annotator methods       ###
###############################

@rpc_method_auth
def get_annotation_task(request):
    """ Gets the annotator's current task """

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
def complete_annotation_task(request, annotation_id, annotation_data, elapsed_time=None):
    """ Complete the annotator's current task, with option to get the next task """

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
    """  """

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
def get_document_content(request, document_id):
    doc = Document.objects.get(pk=document_id)
    if request.user.is_associated_with_document(doc):
        return doc.data
    else:
        raise PermissionError("No permission to access the document")


@rpc_method_auth
def get_annotation_content(request, annotation_id):
    annotation = Annotation.objects.get(pk=annotation_id)
    if request.user.is_associated_with_annotation(annotation):
        return annotation.data
    else:
        raise PermissionError("No permission to access the annotation")



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


###############################
### Utility Methods         ###
###############################

@rpc_method
def get_endpoint_listing(request):
    from .rpcserver import JSONRPCEndpoint
    return JSONRPCEndpoint.endpoint_listing()
