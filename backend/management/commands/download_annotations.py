import json
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from backend.rpcserver import JSONRPCEndpoint
from backend.views import DownloadAnnotationsView
import argparse

class Command(BaseCommand):

    help = "Download annotation data"



    def add_arguments(self, parser):
        parser.add_argument("output_path", type=str, help="Path of file output")
        parser.add_argument("project_id", type=str, help="ID of the project")
        parser.add_argument("doc_type", type=str, help="Document type all, training, test, or annotation")
        parser.add_argument("export_type", type=str, help="Type of export json, jsonl or csv")
        parser.add_argument("anonymize", type=self.str2bool, help="Data should be anonymized or not ")
        parser.add_argument("-j", "--json_format", type=str, help="Type of json format: raw (default) or gate ")
        parser.add_argument("-n", "--num_entries_per_file", type=int, help="Number of entries to generate per file, default 500")


    def handle(self, *args, **options):

        annotations_downloader = DownloadAnnotationsView()

        output_path = options["output_path"]
        project_id = options["project_id"]
        doc_type = options["doc_type"]
        export_type = options["export_type"]
        anonymize = options["anonymize"]
        json_format = options["json_format"] if options["json_format"] else "raw"
        num_entries_per_file = options["num_entries_per_file"] if options["num_entries_per_file"] else 500

        print(f"Writing annotations to {output_path} \n Project: {project_id}\n Document type: {doc_type}\n Export type: {export_type} \n Anonymized: {anonymize} \n Json format:  {json_format} \n Num entries per file: {num_entries_per_file}\n")

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


