import math
import csv
import io
import json
from io import TextIOWrapper
from zipfile import ZipFile
from django.contrib.auth import get_user_model
from django.test import TestCase

from backend.models import Project, Document, Annotation, DocumentType
from backend.tests.test_rpc_server import TestEndpoint
from backend.views import DownloadAnnotationsView


class TestDownloadAnnotations(TestEndpoint):

    def setUp(self):
        self.test_user = get_user_model().objects.create(username="project_creator")
        self.annotators = [get_user_model().objects.create(username=f"anno{i}") for i in range(3)]
        self.project = Project.objects.create(owner=self.test_user)
        self.num_training_docs = 25
        self.num_test_docs = 50
        self.num_docs = 100
        self.num_docs_per_file = 10

        self.create_documents_with_annotations(self.project, self.num_training_docs, DocumentType.TRAINING,
                                               self.annotators)
        self.create_documents_with_annotations(self.project, self.num_test_docs, DocumentType.TEST,
                                               self.annotators)
        self.create_documents_with_annotations(self.project, self.num_docs, DocumentType.ANNOTATION,
                                               self.annotators)

        self.project.refresh_from_db()

    def create_documents_with_annotations(self, project, num_documents, doc_type, annotators):
        for i in range(num_documents):
            document = Document.objects.create(
                project=project,
                data={
                    "id": i,
                    "text": f"Text {i}"

                },
                doc_type=doc_type,
            )

            for annotator in annotators:
                anno = Annotation.objects.create(user=annotator,
                                          document=document,
                                          status=Annotation.COMPLETED,
                                          )
                anno.data = { "text1": "Value1", "checkbox1": ["val1", "val2", "val3"]}

    def test_json_export(self):
        client = self.get_loggedin_client()

        response = client.get(f"/download_annotations/{self.project.id}/training/json/raw/{self.num_docs_per_file}/")
        self.check_json_export_from_response(response,
                                             num_documents_expected=self.num_training_docs,
                                             num_documents_per_file=self.num_docs_per_file)

        response = client.get(f"/download_annotations/{self.project.id}/test/json/raw/{self.num_docs_per_file}/")
        self.check_json_export_from_response(response,
                                             num_documents_expected=self.num_test_docs,
                                             num_documents_per_file=self.num_docs_per_file)

        response = client.get(f"/download_annotations/{self.project.id}/annotation/json/raw/{self.num_docs_per_file}/")
        self.check_json_export_from_response(response,
                                             num_documents_expected=self.num_docs,
                                             num_documents_per_file=self.num_docs_per_file)

    def check_json_export_from_response(self, response, num_documents_expected, num_documents_per_file):
        self.assertEqual(response.status_code, 200)

        with ZipFile(self.get_io_stream_from_streaming_response(response), mode="r") as zip:
            self.check_num_files_in_zip(zip, num_documents_expected, num_documents_per_file)

            num_docs_count = 0
            for file_name in zip.namelist():
                print(f"Checking {file_name}")
                with zip.open(file_name, "r") as file:
                    file_dict = json.loads(file.read())
                    self.assertTrue(isinstance(file_dict, list), "Must be a list of objects")
                    num_docs_count += len(file_dict)

        self.assertEqual(num_docs_count, num_documents_expected)

    def check_num_files_in_zip(self, zip, num_documents_expected, num_documents_per_file):
        """
        Num files must be ceil(num_documents_expected / num_documents_per_file)
        """
        num_files_expected = math.ceil(num_documents_expected / num_documents_per_file)
        self.assertEqual(len(zip.namelist()), num_files_expected, f"Must have {num_files_expected} files")

    def test_jsonl_export(self):

        client = self.get_loggedin_client()
        response = client.get(f"/download_annotations/{self.project.id}/training/jsonl/raw/{self.num_docs_per_file}/")
        self.check_jsonl_export_from_response(response,
                                              num_documents_expected=self.num_training_docs,
                                              num_documents_per_file=self.num_docs_per_file)

        response = client.get(f"/download_annotations/{self.project.id}/test/jsonl/raw/{self.num_docs_per_file}/")
        self.check_jsonl_export_from_response(response,
                                              num_documents_expected=self.num_test_docs,
                                              num_documents_per_file=self.num_docs_per_file)

        response = client.get(f"/download_annotations/{self.project.id}/annotation/jsonl/raw/{self.num_docs_per_file}/")
        self.check_jsonl_export_from_response(response,
                                              num_documents_expected=self.num_docs,
                                              num_documents_per_file=self.num_docs_per_file)

    def check_jsonl_export_from_response(self, response, num_documents_expected, num_documents_per_file):
        self.assertEqual(response.status_code, 200)

        with ZipFile(self.get_io_stream_from_streaming_response(response), mode="r") as zip:
            self.check_num_files_in_zip(zip, num_documents_expected, num_documents_per_file)

            num_docs_count = 0
            for file_name in zip.namelist():
                print(f"Checking {file_name}")
                with zip.open(file_name, "r") as file:
                    for line in file:
                        obj_dict = json.loads(line)
                        self.assertTrue(isinstance(obj_dict, dict), "Object must be a dict")
                        num_docs_count += 1

        self.assertEqual(num_docs_count, num_documents_expected)

    def test_csv_export(self):

        client = self.get_loggedin_client()
        response = client.get(f"/download_annotations/{self.project.id}/training/csv/raw/{self.num_docs_per_file}/")
        self.check_csv_export_from_response(response,
                                              num_documents_expected=self.num_training_docs,
                                              num_documents_per_file=self.num_docs_per_file)

        response = client.get(f"/download_annotations/{self.project.id}/test/csv/raw/{self.num_docs_per_file}/")
        self.check_csv_export_from_response(response,
                                              num_documents_expected=self.num_test_docs,
                                              num_documents_per_file=self.num_docs_per_file)

        response = client.get(f"/download_annotations/{self.project.id}/annotation/csv/raw/{self.num_docs_per_file}/")
        self.check_csv_export_from_response(response,
                                              num_documents_expected=self.num_docs,
                                              num_documents_per_file=self.num_docs_per_file)


    def check_csv_export_from_response(self, response, num_documents_expected, num_documents_per_file):
        self.assertEqual(response.status_code, 200)

        with ZipFile(self.get_io_stream_from_streaming_response(response), mode="r") as zip:
            self.check_num_files_in_zip(zip, num_documents_expected, num_documents_per_file)
            num_docs_count = 0
            for file_name in zip.namelist():
                print(f"Checking {file_name}")
                with zip.open(file_name, "r") as file:
                    reader = csv.reader(TextIOWrapper(file), delimiter=",")
                    for row in reader:
                        print(row)
                        num_docs_count += 1
                    num_docs_count -= 1  # Minus header row

        self.assertEqual(num_docs_count, num_documents_expected)

    def get_io_stream_from_streaming_response(self, response):
        stream = b''.join(response.streaming_content)
        return io.BytesIO(stream)
