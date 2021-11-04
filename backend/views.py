import tempfile
import json
from zipfile import ZipFile
from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View

from backend.models import Project


class MainView(View):
    """
    The main view of the app (index page)
    """

    template_page = "base-vue.html"


    def get(self, request, *args, **kwargs):
        """
        :param request:
        :return:
        """
        context = {
            "settings": settings
        }


        return render(request, self.template_page, context=context)




class DownloadAnnotations(View):

    def generate_download(self, project_id, export_type):

        documents_per_file = 1000
        chunk_size = 512

        project = Project.objects.get(pk=project_id)

        with tempfile.TemporaryFile() as z:
            with ZipFile(z, "w") as zip:
                with tempfile.NamedTemporaryFile("w+") as f:
                    for document in project.documents.all():
                        doc_dict = document.data
                        f.write(json.dumps(doc_dict))
                    f.flush()
                    zip.write(f.name, "something.json")

            # Stream file output

            z.seek(0)
            while True:
                c = z.read(chunk_size)
                if c:
                    yield c
                else:
                    break



    def get(self, request, project_id, export_type):

        response = StreamingHttpResponse(self.generate_download(project_id, export_type))
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = f'attachment;filename="project-{project_id}.{export_type}.zip"'
        return response
