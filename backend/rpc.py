from backend.rpcserver import rpc_method
from backend.models import Project, Document
from backend.utils.serialize import ModelSerializer


serializer = ModelSerializer()

@rpc_method
def create_project():
    proj = Project.objects.create()

    return serializer.serialize(proj)

@rpc_method
def update_project(project_dict):

    proj = serializer.deserialize(Project, project_dict)
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

    return [serializer.serialize(doc) for doc in project.documents.all()]

@rpc_method
def add_project_document(project_id, document):
    project = Project.objects.get(pk=project_id)
    document = Document.objects.create(project=project)

    return

