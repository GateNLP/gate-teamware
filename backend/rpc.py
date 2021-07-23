import logging
import json
from django.contrib.auth import authenticate, get_user_model, login as djlogin, logout as djlogout
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import manager
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.utils import timezone
import gatenlp
from gatenlp import annotation_set
# https://pypi.org/project/gatenlp/

from backend.errors import AuthError
from backend.rpcserver import rpc_method, rpc_method_auth
from backend.models import Project, Document, Annotation
from backend.utils.serialize import ModelSerializer

log = logging.getLogger(__name__)

serializer = ModelSerializer()
User = get_user_model()


#####################################
### Login/Logout/Register Methods ###
#####################################

@rpc_method
def is_authenticated(request):
    context = {
        "isAuthenticated": False,
        "isManager": False,
        "isAdmin": False,
    }
    if request.user.is_authenticated:
        context["isAuthenticated"] = True
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
        djlogin(request, user)
        context["username"] = payload["username"]
        context["isAuthenticated"] = True
        return context
    else:
        raise ValueError("Username already exists")

@rpc_method
def change_password(request, payload):
    user = request.user
    user.set_password(payload.get("password"))
    user.save()
    return        

@rpc_method
def change_email(request, payload):
    user = request.user

    user.email = payload.get("email")
    user.save()
    return

#############################
### User specific methods ###
#############################

@rpc_method
def get_user_details(request):
    user = request.user

    data = {
        "username": user.username,
        "email": user.email,
        "created": user.created,
    }

    user_role = "annotator"
    if user.is_staff:
        user_role = "admin"
    elif user.is_manager:
        user_role = "manager"

    data["user_role"] = user_role

    return data

@rpc_method
def get_user_annotations(request):
    user = request.user

    annotation_out = []
    documents_out = []
    for annotation in Annotation.objects.filter(user=user):
        document = annotation.document

        annotation_out = {
            "id": annotation.pk,
            "annotated_by": annotation.user.username,
            "created": annotation.created,
            "completed": annotation.status_time if annotation.status == Annotation.COMPLETED else None,
            "rejected": annotation.status_time if annotation.status == Annotation.REJECTED else None,
            "timed_out": annotation.status_time if annotation.status == Annotation.TIMED_OUT else None,
            "aborted": annotation.status_time if annotation.status == Annotation.ABORTED else None,
            "times_out_at": annotation.times_out_at,
        }

        doc_out = {
            "id": document.pk,
            "annotations": [annotation_out],
            "created": document.created,
            "completed": document.num_completed_annotations,
            "rejected": document.num_rejected_annotations,
            "timed_out": document.num_timed_out_annotations,
            "pending": document.num_pending_annotations,
            "aborted": document.num_aborted_annotations,
        }

        documents_out.append(doc_out)
    
    return documents_out

##################################
### Project Management Methods ###
##################################

@rpc_method_auth
@transaction.atomic
def create_project(request):
    proj = Project.objects.create()
    proj.owner = request.user
    proj.save()

    return serializer.serialize(proj)


@rpc_method_auth
@transaction.atomic
def update_project(request, project_dict):
    project = serializer.deserialize(Project, project_dict)

    return True


@rpc_method_auth
def get_project(request, pk):
    proj = Project.objects.get(pk=pk)
    return serializer.serialize(proj)


@rpc_method_auth
def get_projects(request):
    projects = Project.objects.all()

    output_projects = []
    for proj in projects:
        out_proj = serializer.serialize(proj)
        out_proj["owned_by"] = proj.owner.username
        out_proj["documents"] = proj.num_documents
        out_proj["completed_tasks"] = proj.num_completed_tasks
        out_proj["pending_tasks"] = proj.num_pending_tasks
        out_proj["rejected_tasks"] = proj.num_rejected_tasks
        out_proj["timed_out_tasks"] = proj.num_timed_out_tasks
        out_proj["aborted_tasks"] = proj.num_aborted_tasks
        out_proj["total_tasks"] = proj.num_annotation_tasks_total
        output_projects.append(out_proj)
    return output_projects


@rpc_method_auth
def get_project_documents(request, project_id):
    project = Project.objects.get(pk=project_id)

    documents_out = []

    documents = project.documents.all()

    # add additional and modified fields to the document json for the frontend
    for document in documents:

        annotations_out = []
        for annotation in document.annotations.all():
            anno_out = {
                "id": annotation.pk,
                "annotated_by": annotation.user.username,
                "created": annotation.created,
                "completed": annotation.status_time if annotation.status == Annotation.COMPLETED else None,
                "rejected": annotation.status_time if annotation.status == Annotation.REJECTED else None,
                "timed_out": annotation.status_time if annotation.status == Annotation.TIMED_OUT else None,
                "aborted": annotation.status_time if annotation.status == Annotation.ABORTED else None,
                "times_out_at": annotation.times_out_at
            }
            annotations_out.append(anno_out)

        doc_out = {
            "id": document.pk,
            "annotations": annotations_out,
            "created": document.created,
            "completed": document.num_completed_annotations,
            "rejected": document.num_rejected_annotations,
            "timed_out": document.num_timed_out_annotations,
            "pending": document.num_pending_annotations,
            "aborted": document.num_aborted_annotations,
        }

        documents_out.append(doc_out)

    return documents_out


@rpc_method_auth
@transaction.atomic
def add_project_document(request, project_id, document_data):
    project = Project.objects.get(pk=project_id)
    document = Document.objects.create(project=project)
    document.data = document_data
    document.save()

    return document.pk


@rpc_method_auth
@transaction.atomic
def add_document_annotation(request, doc_id, annotation):
    document = Document.objects.get(pk=doc_id)
    annotation = Annotation.objects.create(document=document, data=annotation, user=request.user)
    return annotation.pk


@rpc_method_auth
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


@rpc_method_auth
def get_possible_annotators(request):
    annotators = User.objects.filter(annotates=None)
    output = [serializer.serialize(annotator, {"id", "username", "email"}) for annotator in annotators]
    return output


@rpc_method_auth
def get_project_annotators(request, proj_id):
    project = Project.objects.get(pk=proj_id)
    output = [serializer.serialize(annotator, {"id", "username", "email"}) for annotator in project.annotators.all()]
    return output


@rpc_method_auth
@transaction.atomic
def add_project_annotator(request, proj_id, username):
    annotator = User.objects.get(username=username)
    project = Project.objects.get(pk=proj_id)
    project.add_annotator(annotator)
    project.save()
    return True


@rpc_method_auth
@transaction.atomic
def remove_project_annotator(request, proj_id, username):
    annotator = User.objects.get(username=username)
    project = Project.objects.get(pk=proj_id)
    project.remove_annotator(annotator)
    project.save()
    return True


@rpc_method_auth
@transaction.atomic
def get_annotation_task(request):
    """ Gets the annotator's current task """

    # Times out any pending annotation
    Annotation.check_for_timed_out_annotations()

    # Gets project the user's associated with
    user = request.user
    project = user.annotates

    # No project to annotate
    if not project:
        return None

    # User has existing task
    annotation = project.get_current_annotator_task(user)

    # Check that user has not reached quota
    if not annotation:
        # Check that the user has quota first
        if project.annotator_reached_quota(user):
            project.remove_annotator(user)
            return None

        # Return
        annotation = project.assign_annotator_task(user)

    if annotation:
        return annotation.get_annotation_task()

    return None


@rpc_method_auth
@transaction.atomic
def complete_annotation_task(request, annotation_id, annotation_data):
    """ Complete the annotator's current task, with option to get the next task """
    # Gets project the user's associated with
    user = request.user

    annotation = Annotation.objects.get(pk=annotation_id)
    if not annotation.user_allowed_to_annotate(user):
        raise PermissionError(
            f"User {user.username} trying to complete annotation id {annotation_id} that doesn't belong to them")

    if annotation:
        annotation.complete_annotation(annotation_data)


@rpc_method_auth
@transaction.atomic
def reject_annotation_task(request, annotation_id):
    """  """
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
    return doc.data

@rpc_method_auth
def get_annotation_content(request, annotation_id):
    annotation = Annotation.objects.get(pk=annotation_id)
    return annotation.data


###############################
### User Management Methods ###
###############################

@rpc_method_auth
@staff_member_required
def get_all_users(request):
    users = User.objects.all()
    output = [serializer.serialize(user, {"id", "username", "email", "is_manager", "is_staff"}) for user in users]
    return output

@rpc_method_auth
@staff_member_required
def get_user(request, username):
    user = User.objects.get(username=username)

    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_manager": user.is_manager,
        "is_admin": user.is_staff,
    }

    return data

@rpc_method_auth
@staff_member_required
def admin_update_user(request,user_dict):
    user = User.objects.get(id=user_dict["id"])

    user.username = user_dict["username"]
    user.email = user_dict["email"]
    user.is_manager = user_dict["is_manager"]
    user.is_staff = user_dict["is_admin"]
    user.save()

    return user_dict