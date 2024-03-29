import tempfile
import json
import math
import csv
from zipfile import ZipFile
from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from backend.models import Project, Document, DocumentType


class MainView(View):
    """
    The main view of the app (index page)
    """

    template_page = "index.html"


    def get(self, request, *args, **kwargs):
        """
        :param request:
        :return:
        """
        context = {
            "settings": settings
        }


        return render(request, self.template_page, context=context)




class DownloadAnnotationsView(View):


    def get(self, request, project_id, doc_type, export_type, json_format, entries_per_file, anonymize="anonymize"):
        anonymize = False if anonymize=="deanonymize" else True
        if request.user.is_manager or request.user.is_staff or request.user.is_superuser:
            response = StreamingHttpResponse(self.generate_download(project_id, doc_type, export_type, json_format, anonymize, documents_per_file=entries_per_file))

            export_format_extension = ""
            if export_type == "json" or export_type == "jsonl":
                export_format_extension += export_type
                if json_format == "raw" or json_format == "gate":
                    export_format_extension += "-"+json_format
            elif export_type == "csv":
                export_format_extension = export_type

            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = f'attachment;filename="project{project_id:04d}-{export_format_extension}.zip"'
            return response

        return HttpResponse("No permission to access this endpoint", status=401)

    def generate_download(self, project_id, doc_type="all", export_type="json", json_format="raw", anonymize=True, chunk_size=512, documents_per_file=500):

        with tempfile.TemporaryFile() as z:
            self.write_zip_to_file(z, project_id, doc_type, export_type, json_format, anonymize, documents_per_file)

            # Stream file output
            z.seek(0)
            while True:
                c = z.read(chunk_size)
                if c:
                    yield c
                else:
                    break


    def write_zip_to_file(self, file_stream, project_id, doc_type="all", export_type="json", json_format="raw", anonymize=True, documents_per_file=500):

        project = Project.objects.get(pk=project_id)
        with ZipFile(file_stream, "w") as zip:
            all_docs = project.documents.all()
            if doc_type == "training":
                all_docs = project.documents.filter(doc_type=DocumentType.TRAINING)
            elif doc_type == "test":
                all_docs = project.documents.filter(doc_type=DocumentType.TEST)
            elif doc_type == "annotation":
                all_docs = project.documents.filter(doc_type=DocumentType.ANNOTATION)

            num_docs = all_docs.count()
            num_slices = math.ceil(num_docs / documents_per_file)

            for slice_index in range(num_slices):
                start_index = slice_index * documents_per_file
                end_index = ((slice_index + 1) * documents_per_file)
                if end_index >= num_docs:
                    end_index = num_docs

                slice_docs = all_docs[start_index:end_index]

                with tempfile.NamedTemporaryFile("w+") as f:
                    self.write_docs_to_file(f, slice_docs, export_type, json_format, anonymize)
                    zip.write(f.name, f"project-{project_id}-{doc_type}-{slice_index:04d}.{export_type}")

    def write_docs_to_file(self, file, documents, export_type, json_format, anonymize):
        if export_type == "json":
            self.write_docs_as_json(file, documents, json_format, anonymize)
        elif export_type == "jsonl":
            self.write_docs_as_jsonl(file, documents, json_format, anonymize)
        elif export_type == "csv":
            self.write_docs_as_csv(file, documents, anonymize)


    def write_docs_as_json(self, file, documents, json_format, anonymize):
        doc_dict_list = []
        for document in documents:
            doc_dict_list.append(document.get_doc_annotation_dict(json_format, anonymize))

        file.write(json.dumps(doc_dict_list))
        file.flush()

    def write_docs_as_jsonl(self, file, documents, json_format, anonymize):
        for document in documents:
            doc_dict = document.get_doc_annotation_dict(json_format, anonymize)
            file.write(json.dumps(doc_dict) + "\n")
        file.flush()

    def write_docs_as_csv(self, file, documents, anonymize):
        doc_dict_list = []
        keys_list = []
        for document in documents:
            doc_dict_list.append(self.flatten_json(document.get_doc_annotation_dict("csv", anonymize), "."))

        for doc_dict in doc_dict_list:
            keys_list = self.insert_missing_key(keys_list, doc_dict)

        writer = csv.writer(file, delimiter=",", quotechar='"')
        # Header row
        writer.writerow(keys_list)
        # Data
        for doc_dict in doc_dict_list:
            row = []
            for key in keys_list:
                if key in doc_dict:
                    row.append(doc_dict[key])
                else:
                    row.append(None)
            writer.writerow(row)

        file.flush()

    def flatten_json(self, b, delim):
        val = {}
        for i in b.keys():
            if isinstance(b[i], dict):
                get = self.flatten_json(b[i], delim)
                for j in get.keys():
                    val[i + delim + j] = get[j]
            elif isinstance(b[i], list):
                for index, obj in enumerate(b[i]):
                    if isinstance(obj, dict):
                        get = self.flatten_json(obj, delim)
                        for j in get.keys():
                            val[i + delim + str(index) + delim + j] = get[j]
                    else:
                        val[i + delim + str(index)] = obj
            else:
                val[i] = b[i]

        return val

    def insert_missing_key(self, key_list, obj_dict):
        key_list = list(key_list)
        key_set = set(key_list)
        obj_keys = list(obj_dict.keys())
        obj_key_set = set(obj_keys)
        diff_set = obj_key_set.difference(key_set)

        num_obj_keys = len(obj_keys)

        # Do key filling in order
        missing_keys_list = [key for key in obj_keys if key in diff_set]

        for missing_key in missing_keys_list:

            prev_key = None
            next_key = None
            for i, item in enumerate(obj_keys):
                if obj_keys[i] == missing_key:
                    prev_key = obj_keys[i-1] if i > 0 else None
                    next_key = obj_keys[i+1] if i < num_obj_keys - 1 else None
                    break

            if prev_key in key_set:
                prev_key_index = key_list.index(prev_key)
                key_list.insert(prev_key_index + 1, missing_key)
            elif next_key in key_set:
                next_key_index = key_list.index(next_key)
                key_list.insert(next_key_index, missing_key)
            else:
                key_list.insert(-1, missing_key)

            key_set = set(key_list)

        return key_list





