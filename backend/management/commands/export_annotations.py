import json
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from backend.rpcserver import JSONRPCEndpoint
from backend.views import DownloadAnnotationsView
import argparse

class Command(BaseCommand):

    help = "Export zipped annotation data to an file."

    def add_arguments(self, parser):
        parser.add_argument("output_path", type=str, help="Path of file output")
        parser.add_argument("project_id", type=str, help="ID of the project")
        parser.add_argument("-d", "--document_type",
                            type=str,
                            help="Document type of either all, training, test, or annotation. Defaults to all.",
                            choices=["all", "training", "test", "annotation"],
                            default="all",
                            metavar="DOCUMENT_TYPE")
        parser.add_argument("-e", "--export_type",
                            type=str,
                            help="Type of export json, jsonl or csv. Defaults to json.",
                            choices=["json", "jsonl", "csv"],
                            default="json",
                            metavar="EXPORT_TYPE")
        parser.add_argument("-a", "--anonymize", type=self.str2bool, default=True,
                            help="Anonymize data if true. Defaults to true.")
        parser.add_argument("-j", "--json_format", type=str, default="raw",
                            help="Type of json format, raw or gate. Defaults to raw.")
        parser.add_argument("-n", "--num_entries_per_file", type=int, default=500,
                            help="Number of entries to generate per file. Defaults to 500.")



    def handle(self, *args, **options):

        output_path = options["output_path"]
        project_id = options["project_id"]
        doc_type = options["document_type"]
        export_type = options["export_type"]
        anonymize = options["anonymize"]
        json_format = options["json_format"]
        num_entries_per_file = options["num_entries_per_file"]

        print(f"Writing annotations to: {output_path} \n Project id: {project_id}\n Document type: {doc_type}\n Export type: {export_type} \n Anonymized: {anonymize} \n Json format:  {json_format} \n Num entries per file: {num_entries_per_file}\n")

        annotations_downloader = DownloadAnnotationsView()
        with open(output_path, "wb") as z:
            annotations_downloader.write_zip_to_file(file_stream=z,
                                                     project_id=project_id,
                                                     doc_type=doc_type,
                                                     export_type=export_type,
                                                     json_format=json_format,
                                                     anonymize=anonymize,
                                                     documents_per_file=num_entries_per_file)


    def str2bool(self, v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')


