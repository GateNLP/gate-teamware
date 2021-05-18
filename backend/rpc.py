import json

import gatenlp
# https://pypi.org/project/gatenlp/

from backend.rpcserver import rpc_method
from backend.models import Project, Document, Annotation
from backend.utils.serialize import ModelSerializer


serializer = ModelSerializer()

@rpc_method
def create_project():
    proj = Project.objects.create()

    return serializer.serialize(proj)

@rpc_method
def update_project(project_dict):

    project = serializer.deserialize(Project, project_dict)

    for document in json.loads(project_dict["data"]):
        Document.objects.get_or_create(
                    project=project,
                    data=document)

    return True

@rpc_method
def get_project(pk):

    proj = Project.objects.get(pk=pk)
    return serializer.serialize(proj)


@rpc_method
def get_projects():

    projects = Project.objects.all()
    return [serializer.serialize(proj) for proj in projects]

@rpc_method
def get_project_documents(project_id):

    project = Project.objects.get(pk=project_id)

    documents = [serializer.serialize(doc) for doc in project.documents.all()]

    # add additional and modified fields to the document json for the frontend
    for document in documents:
        document["text"] = document["data"]["text"]
        document["annotated_by"] = [annotation["user"] for annotation in document["annotations"]]
        document["annotation_count"] = len(document["annotations"])

    return documents

@rpc_method
def add_project_document(project_id, document):
    project = Project.objects.get(pk=project_id)
    document = Document.objects.create(project=project)

    return document.pk


@rpc_method
def add_document_annotation(doc_id, annotation):
    document = Document.objects.get(pk=doc_id)
    annotation = Annotation.objects.create(document=document, data=annotation)
    return annotation.pk

@rpc_method
def get_annotations(project_id):
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

