import json

from django.contrib.auth import authenticate, get_user_model, login as djlogin, logout as djlogout
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render

import gatenlp
# https://pypi.org/project/gatenlp/

from backend.rpcserver import rpc_method
from backend.models import Project, Document, Annotation
from backend.utils.serialize import ModelSerializer


serializer = ModelSerializer()

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
def login(request,payload):
    context = {}
    user = authenticate(username=payload["username"], password=payload["password"])
    if user is not None:
        djlogin(request, user)
        context["username"] = payload["username"]
        context["isAuthenticated"] = True
        return context
    else:
        context["error"] = "Invalid username or password."

    return JsonResponse(context)

@rpc_method
def logout(request):
    djlogout(request)
    return

@rpc_method
def register(request,payload):
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
        context["error"] = "Username already exists"

    return context


##################################
### Project Management Methods ###
##################################

@rpc_method
def create_project(request):
    proj = Project.objects.create()

    return serializer.serialize(proj)

@rpc_method
def update_project(request, project_dict):
    project = serializer.deserialize(Project, project_dict)

    for document in json.loads(project_dict["data"]):
        Document.objects.get_or_create(
                    project=project,
                    data=document)

    return True

@rpc_method
def get_project(request, pk):

    proj = Project.objects.get(pk=pk)
    return serializer.serialize(proj)


@rpc_method
def get_projects(request):

    projects = Project.objects.all()
    return [serializer.serialize(proj) for proj in projects]

@rpc_method
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

@rpc_method
def add_project_document(request, project_id, document):
    project = Project.objects.get(pk=project_id)
    document = Document.objects.create(project=project)

    return document.pk


@rpc_method
def add_document_annotation(request, doc_id, annotation):
    document = Document.objects.get(pk=doc_id)
    annotation = Annotation.objects.create(document=document, data=annotation)
    return annotation.pk

@rpc_method
def get_annotations(request, project_id):
    """
    Serialize project annotations as GATENLP format JSON using the python-gatenlp interface.
    """
    project = Project.objects.get(pk=project_id)
    annotations = []
    for document in project.documents.all():
        # create a GateNLP Document instance
        doc = gatenlp.Document(text = document.data['text'])
        doc.name = str(document.pk)

        for annotation in document.annotations.all():
            # add an Annotation_Set named as the annotation user
            annset = doc.annset(name = annotation.user.username)
            
            # add the annotation to the annotation set
            annset.add(start = 0,
                        end = len(document.data['text']),
                        anntype = "Document",
                        features=dict(label=annotation.data,_id=annotation.pk),
                        )

        # For each document, append the annotations
        annotations.append(doc.save_mem(fmt="bdocjs"))
    
    return annotations

