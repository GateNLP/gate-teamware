import logging
import json
from django.contrib.auth import authenticate, get_user_model, login as djlogin, logout as djlogout
from django.db import transaction
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.utils import timezone
import gatenlp
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
    context = {}
    if request.user.is_authenticated:
        context["isAuthenticated"] = True
        context["username"] = request.user.username
    else:
        context["isAuthenticated"] = False
    return context


@rpc_method
def login(request, payload):
    context = {}
    user = authenticate(username=payload["username"], password=payload["password"])
    if user is not None:
        djlogin(request, user)
        context["username"] = payload["username"]
        context["isAuthenticated"] = True
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
    return [serializer.serialize(proj) for proj in projects]


@rpc_method_auth
def get_project_documents(request, project_id):
    project = Project.objects.get(pk=project_id)

    documents_out = []

    documents = project.documents.all()

    # add additional and modified fields to the document json for the frontend
    for document in documents:
        doc_out = serializer.serialize(document)
        doc_out["text"] = document.data["text"]
        doc_out["annotated_by"] = []
        for annotation in document.annotations.all():
            if annotation.user:
                doc_out["annotated_by"].append(annotation.user.username)
        doc_out["annotation_count"] = len(document.annotations.all())
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
    project.annotators.add(annotator)
    project.save()
    return True


@rpc_method_auth
@transaction.atomic
def remove_project_annotator(request, proj_id, username):
    annotator = User.objects.get(username=username)
    project = Project.objects.get(pk=proj_id)
    project.annotators.remove(annotator)
    project.save()
    return True


@rpc_method_auth
def get_annotation_task(request):
    """ Gets the annotator's current task """
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
        context = annotation.get_annotation_config()
        return context

    return None


@rpc_method_auth
def complete_annotation_task(request, annotation_id, annotation_data, get_next_task=False):
    """ Complete the annotator's current task, with option to get the next task """
    # Gets project the user's associated with
    user = request.user

    annotation = Annotation.objects.get(pk=annotation_id)
    if annotation.user != user:
        raise PermissionError(
            f"User {user.username} trying to complete annotation id {annotation_id} that doesn't belong to them")

    if annotation:
        annotation.complete_annotation(annotation_data)

    if get_next_task:
        return get_annotation_task(request)

    return None


@rpc_method_auth
def reject_annotation_task(request, annotation_id, get_next_task=False):
    """  """
    # Gets project the user's associated with
    user = request.user

    annotation = Annotation.objects.get(pk=annotation_id)
    if annotation.user != user:
        raise PermissionError(
            f"User {user.username} trying to complete annotation id {annotation_id} that doesn't belong to them")

    if annotation:
        annotation.reject_annotation()

    if get_next_task:
        return get_annotation_task(request)

    return None
