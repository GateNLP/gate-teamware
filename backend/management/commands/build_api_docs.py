import json
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from backend.rpcserver import JSONRPCEndpoint

class Command(BaseCommand):

    help = "Generate a JSON file listing API endpoints"

    def add_arguments(self, parser):
        parser.add_argument('output_dest', type=str)

    def handle(self, *args, **options):


        output_dest = options["output_dest"]

        listing = JSONRPCEndpoint.endpoint_listing()
        for name, props in listing.items():
            listing[name]["all_args"] = ','.join(props["arguments"])


        context = {
            "api_dict": listing
        }

        with open(output_dest, "w") as f:
            f.write(render_to_string("api_docs_template.md", context))


