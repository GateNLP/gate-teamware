import csv
import io
import json
from io import TextIOWrapper
from zipfile import ZipFile
from django.contrib.auth import get_user_model
from django.test import TestCase

from backend.models import Project, Document, Annotation
from backend.tests.test_rpc_server import TestEndpoint
from backend.views import DownloadAnnotationsView

class TestDownloadAnnotations(TestEndpoint):

    def setUp(self):
        self.test_user = get_user_model().objects.create(username="project_creator")
        self.annotators = [get_user_model().objects.create(username=f"anno{i}") for i in range(3)]
        self.project = Project.objects.create(owner=self.test_user)
        for i in range(100):
            document = Document.objects.create(
                project=self.project,
                data={
                    "id": i,
                    "text": f"Text {i}"

                }
            )

            for annotator in self.annotators:
                annotation = Annotation.objects.create(user=annotator,
                                                       document=document,
                                                       status=Annotation.COMPLETED,
                                                       data={
                                                           "text1": "Value1",
                                                           "checkbox1": ["val1", "val2", "val3"]
                                                       })

        self.project.refresh_from_db()

    def test_json_export(self):
        client = self.get_loggedin_client()
        response = client.get(f"/download_annotations/{self.project.id}/json/raw/10/")
        self.assertEqual(response.status_code, 200)

        with ZipFile(self.get_io_stream_from_streaming_response(response), mode="r") as zip:
            self.assertEqual(len(zip.namelist()), 10, "Must have 10 files")
            num_docs_count = 0
            for file_name in zip.namelist():
                print(f"Checking {file_name}")
                with zip.open(file_name, "r") as file:
                    file_dict = json.loads(file.read())
                    self.assertTrue(isinstance(file_dict, list), "Must be a list of objects")
                    num_docs_count += len(file_dict)

        self.assertEqual(num_docs_count, self.project.documents.count())

    def test_jsonl_export(self):

        client = self.get_loggedin_client()
        response = client.get(f"/download_annotations/{self.project.id}/jsonl/raw/10/")
        self.assertEqual(response.status_code, 200)

        with ZipFile(self.get_io_stream_from_streaming_response(response), mode="r") as zip:
            self.assertEqual(len(zip.namelist()), 10, "Must have 10 files")
            num_docs_count = 0
            for file_name in zip.namelist():
                print(f"Checking {file_name}")
                with zip.open(file_name, "r") as file:
                    for line in file:
                        obj_dict = json.loads(line)
                        self.assertTrue(isinstance(obj_dict, dict), "Object must be a dict")
                        num_docs_count += 1

        self.assertEqual(num_docs_count, self.project.documents.count())

    def test_csv_export(self):

        client = self.get_loggedin_client()
        response = client.get(f"/download_annotations/{self.project.id}/csv/raw/10/")
        self.assertEqual(response.status_code, 200)

        with ZipFile(self.get_io_stream_from_streaming_response(response), mode="r") as zip:
            self.assertEqual(len(zip.namelist()), 10, "Must have 10 files")
            num_docs_count = 0
            for file_name in zip.namelist():
                print(f"Checking {file_name}")
                with zip.open(file_name, "r") as file:
                    reader = csv.reader(TextIOWrapper(file), delimiter=",")
                    for row in reader:
                        print(row)
                        num_docs_count += 1
                    num_docs_count -= 1  # Minus header row

        self.assertEqual(num_docs_count, self.project.documents.count())

    def get_io_stream_from_streaming_response(self, response):
        stream = b''.join(response.streaming_content)
        return io.BytesIO(stream)

